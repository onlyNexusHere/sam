#include <math.h>
#include "EnableInterrupt/EnableInterrupt.h"
#include "DualMC33926MotorShield.h"

//#define CIRCUMFERENCE = 2.75 * pi
//#define RESOLUTION = 32 
//resolution = divisions * 2
// SEGMENT_LEN = CIRCUMFERENCE/RESOLUTION = 2.75*pi/32
#define SEGMENT_LEN 0.26998
#define WHEELBASE 6.375

double motor_lookup[] = {0.983240223,0.97752809,0.975903614,0.980392157,0.979166667,0.97037037,0.983870968,0.973913043,0.971698113,0.978947368,0.953488372,0.947368421,0.955223881,0.929824561,0.914893617,0.894736842,0.925925926,0.777777778,0,0,0,0,0,0.684210526,0.857142857,0.894736842,0.956521739,0.964285714,0.954545455,0.960526316,0.965116279,0.978947368,0.981132075,0.982608696,0.984,0.992537313,0.986111111,0.993464052,1.005988024,0.988700565,0.983240223};


volatile long enc_count_left = 0;
volatile long enc_count_right = 0;
DualMC33926MotorShield md;
double posn[] = {0., 0.};
double heading = 0.0;

void setup() {
    // all your normal setup code
    Serial.begin(9600);
    enableInterrupt(2,encoder_isr_left,CHANGE);
    enableInterrupt(5,encoder_isr_left,CHANGE);
    enableInterrupt(3,encoder_isr_right,CHANGE);
    enableInterrupt(6,encoder_isr_right,CHANGE);
    md.init();
    md.setM1Speed(0);
    md.setM2Speed(0);

//    md.setM1Speed(200);
//    md.setM2Speed(r_pwm_to_val(200));
}

void loop(){
  
}
//  do_right_turn();
//  do_left_turn();
//  print_posn();
//  Serial.print("Left: ");
//  Serial.println(enc_count_left);
//  Serial.print("Right: ");
//  Serial.println(enc_count_right);
//  delay(2000);
//  print_pwm_map();
}

void do_right_turn() {
  double dtheta = 0;
  double theta0 = heading;
  while (dtheta < 1.57) {
    dtheta = theta0 - heading;
    md.setM1Speed(360);
    md.setM2Speed(r_pwm_to_val(120));
  }
  md.setM1Speed(0);
  md.setM2Speed(0);
}

void do_left_turn() {
  double dtheta = 0;
  double theta0 = heading;
  while(dtheta > -1.57) {
    Serial.println("TURN");
    dtheta = theta0 - heading;
//    md.setM1Speed(200);
//    md.setM2Speed(r_pwm_to_val(300));
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

void print_pwm_map() {
  Serial.println("Motor 1 Start: 2 second gap");
  Serial.println("speed, encoder start, encoder end");
  for(int i = -400; i <= 400; i+=20) {
    md.setM1Speed(i);
    delay(250);
    Serial.print(i);
    Serial.print(",");
    Serial.print(enc_count_left);
    Serial.print(",");
    delay(2000);
    Serial.println(enc_count_left);
  }
  md.setM1Speed(0);
  Serial.println("Motor 2 Start: 2 second gap");
  Serial.println("speed, encoder start, encoder end");
  for(int i = -400; i <= 400; i+=20) {
    md.setM2Speed(i);
    delay(250);
    Serial.print(i);
    Serial.print(",");
    Serial.print(enc_count_right);
    Serial.print(",");
    delay(2000);
    Serial.println(enc_count_right);
  }
  md.setM2Speed(0);
}

void print_posn(){
  Serial.print("x: ");
  Serial.print(posn[0]);
  Serial.print(" y: ");
  Serial.print(posn[1]);
  Serial.print(" theta: ");
  Serial.println(heading);
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
