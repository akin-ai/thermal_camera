#include "sharpIR.h"

DistanceSensor LeftDistanceSensor(16, 'L', 40);
DistanceSensor RightDistanceSensor(A3, 'R', 40);

void setup(){
  Serial.begin(9600);
  
}
void loop(){
    float x = LeftDistanceSensor.receive_data();
    float y = RightDistanceSensor.receive_data();
    Serial.println("\n x = ");
    Serial.println(x);
//    Serial.println("\n y = ");
//    Serial.println(y);
    
    delay(100);
    }
