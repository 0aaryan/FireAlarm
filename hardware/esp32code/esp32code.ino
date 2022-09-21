#include <Adafruit_Sensor.h>
#include "DHT.h"
#define DHTTYPE DHT11   
#define DHTPIN 14
int Gas_analog = 13;  
int Fire_analog = 12; 
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();  

}

void loop() {
    delay(2000);
  int gassensorAnalog = analogRead(Gas_analog);
  int firesensorAnalog = analogRead(Fire_analog);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  // if (isnan(h) || isnan(t)) {
  //   Serial.println(F("Failed to read from DHT sensor!"));
  //   return;
  // }

  float hic = dht.computeHeatIndex(t, h, false);
  Serial.print("Gas Sensor: ");
  Serial.print(gassensorAnalog);
  Serial.print("\tFire Sensor: ");
  Serial.print(firesensorAnalog);
  Serial.print("\t Temprature: ");
  Serial.print(t);
  Serial.print("\t Humidity: ");
  Serial.print(h);
  Serial.print("\t Heat Index: ");
  Serial.print(hic);
  Serial.print("\n");


}