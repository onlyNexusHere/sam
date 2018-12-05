#include <math.h>
#include "EnableInterrupt/EnableInterrupt.h"
#include "DualMC33926MotorShield.h"

//#define CIRCUMFERENCE = 2.75 * pi
//#define RESOLUTION = 32 
//resolution = divisions * 2
// SEGMENT_LEN = CIRCUMFERENCE/RESOLUTION = 2.75*pi/32
#define SEGMENT_LEN 0.26998
#define WHEELBASE 6.375

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
}

void loop(){
  go_straight(43);
  turn_left_enc();
  go_straight(17.5);

  // go_straight(20.5);
  // turn_right_enc();
  // go_straight(42.5);
}

void go_straight(double dist_inches) {
  double startx = posn[0];
  double starty = posn[1];
  double prev = 0.0;
  double K = 0.001;
  double B = 0.0001;
  int start_lc = enc_count_left;
  int start_rc = enc_count_right;
  double mL = 130;
  double mR = 130;
  md.setM1Speed((int)mL);
  md.setM2Speed((int)mR);
  while(distance(startx, starty, posn[0], posn[1]) < dist_inches) {
    int error = (enc_count_left - start_lc) - (enc_count_right - start_rc);
    double errorDD = -K*error-B*(error-prev);
    mL = mL + errorDD;
    mR = mR - errorDD;
    md.setM1Speed((int)mL);
    md.setM2Speed((int)mR);
    prev = adjustment
  }
}

void turn_right_enc() {
  double prev = 0.0;
  double K = 0.001;
  double B = 0.0001;
  int start_lc = enc_count_left;
  int start_rc = enc_count_right;
  double mL = 330;
  double mR = 110;
  md.setM1Speed((int)mL);
  md.setM2Speed((int)mR);
  double dtheta = 0;
  double theta0 = heading;
  while (dtheta < 1.57) {
    // Left wheel travels 3x as far as right wheel
    int error = (enc_count_left - start_lc) - 3*(enc_count_right - start_rc);
    double errorDD = -K*error-B*(error-prev);
    mL = mL + errorDD;
    mR = mR - errorDD;
    md.setM1Speed((int)mL);
    md.setM2Speed((int)mR);
    prev = adjustment
    dtheta = theta0 - heading;
  }
}

void turn_left_enc() {
  double prev = 0.0;
  double K = 0.001;
  double B = 0.0001;
  int start_lc = enc_count_left;
  int start_rc = enc_count_right;
  double mL = 140;
  double mR = 210;
  md.setM1Speed((int)mL);
  md.setM2Speed((int)mR);
  double dtheta = 0;
  double theta0 = heading;
  while(dtheta > -1.57) {    // Left wheel travels 2/3x as far as right wheel
    int error = 3*(enc_count_left - start_lc) - 2*(enc_count_right - start_rc);
    double errorDD = -K*error-B*(error-prev);
    mL = mL + errorDD;
    mR = mR - errorDD;
    md.setM1Speed((int)mL);
    md.setM2Speed((int)mR);
    prev = adjustment
    dtheta = theta0 - heading;
  }
}

double distance(double x0, double y0, double x1, double y1) {
  return math.sqrt(math.pow(x0 - x1, 2), math.pow(y0 - y1, 2));
}

