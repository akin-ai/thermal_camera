#include "sharpIR.h"

DistanceSensor LeftDistanceSensor(16, 'L', 40);
DistanceSensor RightDistanceSensor(A3, 'R', 40);

void setup(){
  Serial.begin(9600);
  
}
void loop(){
    float x = (LeftDistanceSensor.receive_data()+1.0536)/1.2695;
    float y = (RightDistanceSensor.receive_data()+10.536)/12.695;
    Serial.println("\n x = ");
    Serial.println(x);
//    Serial.println("\n y = ");
//    Serial.println(y);
    
    delay(500);
    }
