#include <Wire.h>

// Device HEX codes - put in an matrix at a later point
byte kitchenLights = 0x01;
byte livingRoomLights = 0x02;
byte bedroom1Lights = 0x03;
byte bedroom2Lights = 0x04;
byte bedroom3Lights = 0x05;
byte frontDoorLights = 0x06;
byte backDoorLights = 0x07;
byte serverRoomLights = 0x08;
byte ServerFans = 0x09;
byte drivewayLights = 0x10;

byte ELC = 0xFF;
byte off = 0xA0;
byte on = 0xA1;
byte data[] = "";
int howMany;
int dataReceived;

void setup()
{
  Wire.begin(4);
  Wire.onReceive(receiveEvent);
  Serial.begin(9600);
}

void loop()
{
  if (dataReceived > 0) {
    howMany = dataReceived;
    Serial.print(howMany);
    Serial.println(" bytes of data received...processing");
    processData(data, howMany);
    dataReceived = 0;
  }
}

void processData(byte data[], int howMany) {
  for (int i=0; i < howMany; i++) {
    if (data[i] == ELC){
      Serial.println("Aborting...");
      break;
    }
  } 
  if (data[0] == kitchenLights) {
    Serial.print("Kitchen Lighting selected. Action: ");
    if (data[1] == on) { Serial.println("Turn On"); }
    if (data[1] == off) { Serial.println("Turn Off"); }
  }
    if (data[0] == livingRoomLights) {
    Serial.print("Living Room Lighting selected. Action: ");
    if (data[1] == on) { Serial.println("Turn On"); }
    if (data[1] == off) { Serial.println("Turn Off"); }
  }
    if (data[0] == bedroom1Lights) {
    Serial.print("Bedroom #1 Lighting selected. Action: ");
    if (data[1] == on) { Serial.println("Turn On"); }
    if (data[1] == off) { Serial.println("Turn Off"); }
  }
    if (data[0] == bedroom2Lights) {
    Serial.print("Bedroom #2 Lighting selected. Action: ");
    if (data[1] == on) { Serial.println("Turn On"); }
    if (data[1] == off) { Serial.println("Turn Off"); }
  }
    if (data[0] == bedroom3Lights) {
    Serial.print("Bedroom #3 Lighting selected. Action: ");
    if (data[1] == on) { Serial.println("Turn On"); }
    if (data[1] == off) { Serial.println("Turn Off"); }
  }
    if (data[0] == frontDoorLights) {
    Serial.print("Front Door Lighting selected. Action: ");
    if (data[1] == on) { Serial.println("Turn On"); }
    if (data[1] == off) { Serial.println("Turn Off"); }
  }
    if (data[0] == backDoorLights) {
    Serial.print("Back door Lighting selected. Action: ");
    if (data[1] == on) { Serial.println("Turn On"); }
    if (data[1] == off) { Serial.println("Turn Off"); }
  }
    if (data[0] == serverRoomLights) {
    Serial.print("Server Room Lighting selected. Action: ");
    if (data[1] == on) { Serial.println("Turn On"); }
    if (data[1] == off) { Serial.println("Turn Off"); }
  }
    if (data[0] == serverFans) {
    Serial.print("Server Fans selected. Action: ");
    if (data[1] == on) { Serial.println("Turn On"); }
    if (data[1] == off) { Serial.println("Turn Off"); }
  }
    if (data[0] == drivewayLights) {
    Serial.print("Driveway Lighting selected. Action: ");
    if (data[1] == on) { Serial.println("Turn On"); }
    if (data[1] == off) { Serial.println("Turn Off"); }
  }
}

void receiveEvent(int howMany)
{
  //byte data[howMany];
  //Serial.println("Debug Spot 2");
  while(Wire.available())
  {
    for (int i=0; i <= howMany; i++) {
      data[i] = Wire.read();
    }
    dataReceived = howMany;
  }
}
