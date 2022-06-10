#include "new_global_vars.h"
#include "Distance_Sensor.h"
#include "IMU.h"
#include "TCA.h"
#include "AS7262.h"
#include "motors.h"
#include "rescueServo.h"
#include "limitswitch.h"

//N E S W --> South always 0
void setup() {
  delay(100);
  Serial3.begin(9600);
  Serial2.begin(9600);
  Wire.begin();
  ports[LEFT].setMotorSpeed(0);
  ports[RIGHT].setMotorSpeed(0);
  setupLightSensors();
  setupSwitches();

  // macros
  INIT_INTERRUPT_LEFT;
  INIT_INTERRUPT_RIGHT;

  ports[RIGHT].backwards = true;


  Serial3.println("--------------------STARTING NOW--------------------");
  setupSensors2();
  initIMU();
  delay(1000);
  Serial3.println('a');
  Serial2.write('a');
  sendWallValues(getSensorReadings(2), getSensorReadings(0), getSensorReadings(1));
}

void loop() {
 // triangulation(getSensorReadings(1), getSensorReadings(0));
//turnRight(90);
//delay(1000);
//turnAbs(270);
//while(true);
  //while(true) displayIMU();

//  goForwardPID(30);
//  while(true);
  
  if (Serial2.available()) {
    delay(1);
    char incoming_byte = Serial2.read();
    delay(1);
    Serial3.print("Message detected: ");
    Serial3.println(incoming_byte);
    switch (incoming_byte) {
      case '{':
       // Serial3.println("read {");
        break;
      case 'W':
        rampMoveForward('u');
        alignFront();
        finishedRamp=0;
        delay(1);
        Serial2.write(';');
        delay(1);
        break;
      case 'M':
        rampMoveForward('d');
        alignFront();
        finishedRamp=0;
        delay(1);
        Serial2.write(';');
        delay(1);
        break;
      case 'F':
        //get rid of semicolon
        delay(1);
        Serial2.read();
        delay(1);
        
       // Serial3.println("forward!");
        //goForwardTilesPID(1);
        if(triangulation(getSensorReadings(1), getSensorReadings(0))){
        alignFront();
        delay(1);
        Serial2.write(';');
        delay(1);
        Serial3.println(';');
        }
        //isHeat = false;
        Serial3.println("finished going forward");
        break;
        
      case 'L':
        //get rid of semicolon
        delay(1);
        Serial2.read();
        delay(1);
        
        //Serial3.println("left!");
        turnAbs('l');
        //if(!isHeat){
        delay(1);
        Serial2.write(';');
        delay(1);
        Serial3.println(';');
//        }
//        isHeat=false;
        break;

      case 'R':
        //get rid of semicolon
        delay(1);
        Serial2.read();
        delay(1);
        
       // Serial3.println("right!");
        turnAbs('r');
        //if(!isHeat){
        delay(1);
        Serial2.write(';');
        delay(1);
        Serial3.println(';');
//        }
//        isHeat=false;
        break;
        
      case '}':
        Serial3.println("}");
        if(finishedRamp==1)
          Serial2.write('u');
        else if(finishedRamp==2)
          Serial2.write('d');
        finishedRamp=0;
        delay(15);
        sendWallValues(getSensorReadings(2), getSensorReadings(0), getSensorReadings(1));
        break;
      case 'Y': // 1 kit
        Serial3.println("red/yellow");
        RGB_color(255, 0, 0, 1, 'R'); // Red
        //dropKits('R', 1);
        break;

      case 'G': // 0 kits
        Serial3.println("green");
        RGB_color(0, 255, 0, 0, 'R'); // Green
        break;

      case 'H': // 3 kits
        Serial3.println("H");
        RGB_color(0, 0, 255, 3, 'R'); // Blue
        //dropKits('R', 3);
        break;

      //turn left
      case 'S': // 2 kits
        Serial3.println("S");
        RGB_color(0, 255, 255, 2, 'R'); // Cyan
        //dropKits('R', 2);
        break;

      //turn right
      case 'U': // 0 kits
        Serial3.println("U");
        RGB_color(255, 0, 255, 0, 'R'); // Magenta
        break;
      case 'y': // 1 kit
        Serial3.println("red/yellow");
        RGB_color(255, 0, 0, 1, 'L'); // Red
        //dropKits('L', 1);
        break;

      case 'g': // 0 kits
        Serial3.println("green");
        RGB_color(0, 255, 0, 0, 'L'); // Green
        break;

      case 'h': // 3 kits
        Serial3.println("H");
        RGB_color(0, 0, 255, 3, 'L'); // Blue
        //dropKits('L', 3);
        break;

      //turn left
      case 's': // 2 kits
        Serial3.println("S");
        RGB_color(0, 255, 255, 2, 'L'); // Cyan
        //dropKits('L', 2);
        break;

      //turn right
      case 'u': // 0 kits
        Serial3.println("U");
        RGB_color(255, 0, 255, 0, 'R'); // Magenta
        break;
        
      default:
        Serial3.print("hmmm wut is this: ");
        Serial3.println(incoming_byte);
        break;
    }
  }
}
