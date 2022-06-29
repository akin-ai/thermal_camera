#ifndef SharpIR_h
#define SharpIR_h

#define OBSTACLE_DISTANCE 1000
#define DISTANCE_SAMPLES 25
#define OFFSET_DISTANCE 2

#include "Arduino.h"

class DistanceSensor {
  private:
    int pin;
    int alert_flag;
    int alert_until;
    bool alert;
  public:
    char position;
    DistanceSensor(int pin, char position, int alert_until);
    int values[DISTANCE_SAMPLES];
    
    void init();
    int receive_data();
    void alert_flag_check(int distance);
    float median(int a[], int array_size);
    void sort(int a[], int array_size);
        
};

#endif
