#ifndef _MOTORIMU_H_
#define _MOTORIMU_H_

#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include "motors.h"
#include "rescueServo.cpp"


void initIMU();
void reset();
void turnRight(int deg);
void turnLeft(int deg);
void turnRightPID(int deg);
void turnLeftPID(int deg);
void turnAbs(char t);
void turnAbs(int);

extern int resetPinIMU;
extern Adafruit_BNO055 bno;

#endif
