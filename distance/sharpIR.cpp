#define OBSTACLE_DISTANCE 1000
#define DISTANCE_SAMPLES 25
#define OFFSET_DISTANCE 2
#include "SharpIR.h"
DistanceSensor::DistanceSensor(int pin, char position, int alert_until) {
      this->position = position;
      this->pin = pin;
      this->alert_until = alert_until;
      init();
}
    void DistanceSensor::init() {
      pinMode(pin, INPUT);
    }
    
    float DistanceSensor::receive_data() {
      float distanceCM;
      // Store the Distance sensor values 
      for (int i=0; i<DISTANCE_SAMPLES; i++){
        values[i] = analogRead(pin);
      }
      sort(values, DISTANCE_SAMPLES); 
      float final_value = median(values, DISTANCE_SAMPLES); 
      distanceCM = 60.374  * pow(map(final_value, 0, 1023, 0, 5000)/1000.0, -1.16);

      if(distanceCM<20){
        distanceCM = (distanceCM+2.08)/1.406;  //calib for <20 cm
      }
      else{
        distanceCM = (distanceCM+1.0536)/1.2695;  //calib for 20-100cm
      }
      alert_flag_check(distanceCM);
      return distanceCM;
    }
    void DistanceSensor::alert_flag_check(int distance){
      if(distance > this->alert_until){
        this->alert_flag--;
        if(this->alert_flag <= 0){
          this->alert_flag = 3;
          this->alert = true;
          Serial.print("Alert in: ");
          Serial.println(this->position);
        }
      }
      
    }
    float DistanceSensor::median(int a[], int array_size){
      float median = 0; 
      sort(a, array_size);
      if(array_size % 2 != 0){
        median = a[array_size/2];
      }else{
        median = a[(array_size-1)/2]+a[array_size/2]/2.0;   
      }
      return median; 
      
    }
   void DistanceSensor::sort(int a[], int array_size) {
      for(int i=0; i<(array_size); i++) {
          bool flag = true;
          for(int j=0; j<(array_size-1); j++) {
              if(a[j] > a[j+1]) {
                  int k = a[j];
                  a[j] = a[j+1];
                  a[j+1] = k;
              }
          }
      }
  }
