#ifndef TCS_DEF
#define TCS_DEF
#include "Adafruit_TCS34725.h"
#include "TCA.h"
void setupTCSSensors();
void getValues();
void detectTiles();
extern Adafruit_TCS34725 tcs;
#endif
