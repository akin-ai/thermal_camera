/*
  Output the temperature readings to all pixels to be read by a Processing visualizer
  By: Nathan Seidle
  SparkFun Electronics
  Date: May 22nd, 2018
  License: MIT. See license file for more information but you can
  basically do whatever you want with this code.

  Feel like supporting open source hardware?
  Buy a board from SparkFun! https://www.sparkfun.com/products/14769

  This example outputs 768 temperature values as fast as possible. Use this example
  in conjunction with our Processing visualizer.

  This example will work with a Teensy 3.1 and above. The MLX90640 requires some
  hefty calculations and larger arrays. You will need a microcontroller with 20,000
  bytes or more of RAM.

  This relies on the driver written by Melexis and can be found at:
  https://github.com/melexis/mlx90640-library

  Hardware Connections:
  Connect the SparkFun Qwiic Breadboard Jumper (https://www.sparkfun.com/products/14425)
  to the Qwiic board
  Connect the male pins to the Teensy. The pinouts can be found here: https://www.pjrc.com/teensy/pinout.html
  Open the serial monitor at 115200 baud to see the output
*/

#include <Wire.h>

#include "MLX90640_API.h"
#include "MLX90640_I2C_Driver.h"
#include "Arduino.h"

paramsMLX90640 mlx90640;

void setup()
{
  mlx90640 = MLX90640init(mlx90640);
}

void loop()
{
  mlx90640 = MLX90640_Send(mlx90640);
}
