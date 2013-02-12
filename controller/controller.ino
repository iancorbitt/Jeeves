// Wire Slave Receiver
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Receives data as an I2C/TWI slave device
// Refer to the "Wire Master Writer" example for use with this

// Created 29 March 2006

// This example code is in the public domain.


#include <Wire.h>

void setup()
{
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
}

void loop()
{
  delay(100);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany)
{
  byte data[howMany];
  while(Wire.available()) // loop through all but the last
  {
    for (int i=0; i <= howMany; i++){
      data[i] = Wire.read(); // receive byte as a character
      //byte command = Wire.read();
      //Serial.print("DEV: 0x");
      //Serial.println(device, HEX);
    }
  }
  for (int i=0; i<= howMany; i++){
    Serial.print("Field ");
    Serial.print(i);
    Serial.print(": 0x");
    Serial.println(data[i], HEX);
  }
}
