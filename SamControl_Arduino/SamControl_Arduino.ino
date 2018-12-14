/* KEY
// m s1 s2 => set motors to speends s1 and s2 respectively (s1, s2 should be ints)
// i => Requests the arduino to send quadrature data over serial
// r => Resets quadrature to 0,0
// x => left_routine
// y => right_routine
// k => Reset speeds to 0
// p => Requests the arduino to send over ping data
*/

#include <math.h>
#include "EnableInterrupt/EnableInterrupt.h"
#include "DualMC33926MotorShield.h"
#define SEGMENT_LEN 0.26998
#define WHEELBASE 6.375
#define PING 11

int m1Speed = 0;
int m2Speed = 0;

volatile long enc_count_left = 0;
volatile long enc_count_right = 0;
int count = 0;

DualMC33926MotorShield md;
double posn[] = {0., 0.};
double heading = 0.0;

void stopIfFault() {
  if (md.getFault()) {
    Serial.println("fault");
    while(1);
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

// Resets the encoder position to 0,0
void resetEncoder(){
  posn[0] = 0.;
  posn[1] = 0.;
  heading = 0;
}

void setup() {
  Serial.begin(115200);
  Serial.flush();
  Serial.setTimeout(250);
  md.init();
  enableInterrupt(2,encoder_isr_left,CHANGE);
  enableInterrupt(5,encoder_isr_left,CHANGE);
  enableInterrupt(3,encoder_isr_right,CHANGE);
  enableInterrupt(6,encoder_isr_right,CHANGE);
  setSpeedsWrap(0, 0);
  pinMode(PING, OUTPUT);
  digitalWrite(PING, LOW);
}

String incomingByte = "";
String m[12];

int i = 0;

// Can receive the following commands from pi:
// 1. "m 100 200" =>  100: left motor to 100, 200: right motor 200
// 2. "i" => returns "ir 1 2 3\n" where 1: x, 2: y, 3: heading
long timeout = 0;
unsigned long previousMillis = 0;
const long interval = 2000;
void loop() {
  if (Serial.available() > 0) {
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

    if(m[0].equals("m") || m[0].equals("m\n")){
       setSpeedsWrap(m[1].toInt(), m[2].toInt());
    }

    //If PI requesting Quadrature data
    else if (m[0].equals("i") || m[0].equals("i\n")){
        Serial.flush();
        String pos = getPosition();

        char x[100] ;
        pos.toCharArray(x, 100);
        Serial.println(x);
    }

    // Send r to reset the quadrature to 0,0
    else if(m[0].equals("r") || m[0].equals("r\n")) {
      resetEncoder();
    }

    else if(m[0].equals("k") || m[0].equals("k\n")) {
      m1Speed = 0;
      m2Speed = 0;
      setSpeedsWrap(0, 0);
    }

    else if(m[0].equals("a") || m[0].equals("a\n")) { // left turn routine 
      left_routine();
    }
    else if(m[0].equals("d") || m[0].equals("d\n")) { // right turn routine
      right_routine();
    }
    else if(m[0].equals("w") || m[0].equals("w\n")) { // straight turn routine
      straight_routine();
    }
  }

  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    int distance = ping_distance();
    int m1Cache = m1Speed;
    int m2Cache = m2Speed;
    if(distance > 0 && distance < 15) {
      setSpeedsWrap(0, 0);
      while(distance < 15 && distance > 0) {
        distance = ping_distance();
        delay(100);
      }
      setSpeedsWrap(m1Cache, m2Cache);
    }
  }
}

void setSpeedsWrap(int speedL, int speedR) {
  m1Speed = speedL;
  m2Speed = speedR;
  md.setSpeeds(m1Speed, m2Speed);
}

long ping_distance() {
  long duration, dist;

  // The PING is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(PING, OUTPUT);
  digitalWrite(PING, LOW);
  delayMicroseconds(2);
  digitalWrite(PING, HIGH);
  delayMicroseconds(5);
  digitalWrite(PING, LOW);
  pinMode(PING, INPUT);
  duration = pulseIn(PING, HIGH, 5000);
  if(duration == 0) {
    dist = -1;
  } else {
    dist = microsecondsToCentimeters(duration);
  }
  return dist;
}

long microsecondsToCentimeters(long microseconds) {
  return microseconds / 29 / 2;
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

void left_routine() {
  go_straight(11);
  do_left_turn();
  setSpeedsWrap(0, 0);
  Serial.println("map ready");
}

void right_routine() {
  go_straight(11);
  do_right_turn();
  setSpeedsWrap(0, 0);
  Serial.println("map ready");
}

void straight_routine() {
  go_straight(32);
  Serial.println("map ready");
}

void go_straight(double distance) {
  resetEncoder();
  setSpeedsWrap(164, 162);
  while(posn[0] < distance) { // Intersection is about 20 inches long
    Serial.print("debug");
    Serial.println(distance);
    delay(10);
  }
  setSpeedsWrap(0, 0);
}

void do_right_turn() {
  double dtheta = 0;
  double theta0 = heading;
  setSpeedsWrap(230, 70);
  while (dtheta < 1.57) {
    dtheta = theta0 - heading;
    Serial.print("debug ");
    Serial.println(dtheta);
    delay(10);
  }
  setSpeedsWrap(0, 0);
}

void do_left_turn() {
  double dtheta = 0;
  double theta0 = heading;
  setSpeedsWrap(150, 240);
  while(dtheta > -1.57) {
    dtheta = theta0 - heading;
    Serial.print("debug");
    Serial.println(dtheta);
    delay(10);
  }
  setSpeedsWrap(0, 0);
}


