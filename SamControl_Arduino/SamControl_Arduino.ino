#include <math.h>
#include "EnableInterrupt/EnableInterrupt.h"
#include "DualMC33926MotorShield.h"

//#define CIRCUMFERENCE = 2.75 * pi
//#define RESOLUTION = 32 
//resolution = divisions * 2
// SEGMENT_LEN = CIRCUMFERENCE/RESOLUTION = 2.75*pi/32
#define SEGMENT_LEN 0.26998
#define WHEELBASE 6.375
#define PING 7

double motor_lookup[] = {0.983240223,0.97752809,0.975903614,0.980392157,0.979166667,0.97037037,0.983870968,0.973913043,0.971698113,0.978947368,0.953488372,0.947368421,0.955223881,0.929824561,0.914893617,0.894736842,0.925925926,0.777777778,0,0,0,0,0,0.684210526,0.857142857,0.894736842,0.956521739,0.964285714,0.954545455,0.960526316,0.965116279,0.978947368,0.981132075,0.982608696,0.984,0.992537313,0.986111111,0.993464052,1.005988024,0.988700565,0.983240223};


volatile long enc_count_left = 0;
volatile long enc_count_right = 0;
int count = 0;

DualMC33926MotorShield md;
double posn[] = {0., 0.};
double heading = 0.0;

void stopIfFault()
{
  if (md.getFault())
  {
    Serial.println("fault");
    while(1);
  }
} 



void setup() {
    // all your normal setup code
    Serial.begin(115200);
    Serial.flush();
    Serial.setTimeout(250);
    //Serial.println("Dual MC33926 Motor Shield");
    md.init();
    enableInterrupt(2,encoder_isr_left,CHANGE);
    enableInterrupt(5,encoder_isr_left,CHANGE);
    enableInterrupt(3,encoder_isr_right,CHANGE);
    enableInterrupt(6,encoder_isr_right,CHANGE);
    md.setM1Speed(0);
    md.setM2Speed(0);
    //noInterrupts();

}

String incomingByte = "";
String m[12];

int i = 0;

// Can receive the following commands from pi:
// 1. "m 1 100 200" => m: motor, 1/0: on/off, 100: left motor to 100, 200: right motor 200
// 2. "ir" => returns "ir 1 2 3\n" where 1: x, 2: y, 3: heading
long timeout = 0;
void loop(){

    if (Serial.available()) {
      String string = Serial.readString();
      
      char str[12];
      string.toCharArray(str, 12);
      char* ptr = strtok(str, " ");

      i = 0;
      while(ptr != NULL) {
        //Serial.println(ptr);
        m[i] = ptr;
        i = i + 1;
        ptr = strtok(NULL, " ");
      }
      Serial.flush();


    if(m[0].equals("m")){
       md.setSpeeds(m[1].toInt(), m[2].toInt());
    }
    
    
    //If PI requesting Quadrature data
    else if (m[0].equals("i")){
        Serial.flush();
        String pos = getPosition();

        char x[100] ;
        pos.toCharArray(x, 100);
        Serial.println(x);
    }
    else if(m[0].equals("x")){
      do_left_turn();
    }
    else if(m[0].equals("y")){
      do_right_turn();
    } 
    else if (m[0].equals("p")) {
      Serial.println("ping " + get_distance());
    }
    }
}

void encoder_isr_left() {
  // pins 2 and 5
    static int8_t lookup_table[] = {0,-1,1,0,1,0,0,-1,-1,0,0,1,0,1,-1,0};
    static uint8_t enc_val_l = 0;
    uint8_t ir1 = ((PIND & 0b0100) >> 2) | ((PIND & 0b100000) >> 4);

    enc_val_l = enc_val_l << 2;
    enc_val_l = enc_val_l | ir1;

    int delta = lookup_table[enc_val_l & 0b1111];
    enc_count_left = enc_count_left + delta;
    double dx = delta * 0.5 * SEGMENT_LEN;
    double dt = atan2(-dx, WHEELBASE/2);
    heading += dt;
    posn[0] = posn[0] + dx*cos(heading);
    posn[1] = posn[1] + dx*sin(heading);
}

void encoder_isr_right() {
    // pins 3 and 6
    static int8_t lookup_table[] = {0,-1,1,0,1,0,0,-1,-1,0,0,1,0,1,-1,0};
    static uint8_t enc_val_r = 0;
    uint8_t ir2 = ((PIND & 0b1000) >> 3) | ((PIND & 0b1000000) >> 5);

    enc_val_r = enc_val_r << 2;
    enc_val_r = enc_val_r | ir2;
    
    int delta = lookup_table[enc_val_r & 0b1111];
    enc_count_right = enc_count_right + delta;
    double dx = delta * 0.5 * SEGMENT_LEN;
    double dt = atan2(dx, WHEELBASE/2);
    heading += dt;
    posn[0] = posn[0] + dx*cos(heading);
    posn[1] = posn[1] + dx*sin(heading);
}

void get_distance() {
  pinMode(PING, OUTPUT);
  digitalWrite(PING, LOW);
  delayMicroseconds(2);
  digitalWrite(PING, HIGH);
  delayMicroseconds(5);
  digitalWrite(PING, LOW);

  pinMode(PING, INPUT);
  duration = pulseIn(PING, HIGH);

  // convert the time into a distance
  inches = microsecondsToInches(duration);
  return inches
}

void do_right_turn() {
  double dtheta = 0;
  double theta0 = heading;
  while (dtheta < 1.57) {
    Serial.println("TURN");
    dtheta = theta0 - heading;
    md.setM1Speed(360);
    md.setM2Speed(r_pwm_to_val(120));
  }
  Serial.println("STOP");
  md.setM1Speed(0);
  md.setM2Speed(0);
}

void do_left_turn() {
  double dtheta = 0;
  double theta0 = heading;
  while(dtheta > -1.57) {
    Serial.println("TURN");
    dtheta = theta0 - heading;
    md.setM1Speed(200);
    md.setM2Speed(r_pwm_to_val(300));
  }
  Serial.println("STOP");
  md.setM1Speed(0);
  md.setM2Speed(0);

}

int r_pwm_to_val(int pwm) {
  if (pwm % 20) {
    return -1;
  }
  int idx = (pwm + 400) / 20;
  return pwm * motor_lookup[idx];
}


// Calculates the distance between the starting position of the robot and the current position
double distance(){
  double x = posn[0];
  double y = posn[1];
  return sqrt(x*x + y*y);
}

// Returns the position in the following format: 
// "ir 1 2 3\n" where 1: x, 2: y, 3: heading
String getPosition(){
  return "ir " + String(posn[0]) + " "+ String(posn[1]) + " " + String(heading) + "\n";
}

long microsecondsToInches(long microseconds) {
  return microseconds / 74 / 2;
}
