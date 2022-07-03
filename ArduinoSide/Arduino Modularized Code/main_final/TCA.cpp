#include "TCA.h"

//selects MUX port
uint8_t lastPort = 20;
void tcaselect(uint8_t i) {//make static var
  if(i==lastPort) return;
  if (i > 7) return;

  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();
  lastPort = i;
}
