#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_Sensor.h>
#include "DHT.h"
#define DHTTYPE DHT11   
#define DHTPIN 14
int Gas_analog = 32;  
int Fire_analog = 33; 
int Buzzer=12;
int alert=0;


String mongoid="636f650ac98306f293a7584e";
const char* ssid = "Aryan";
const char* password = "Aryan@1234";



DHT dht(DHTPIN, DHTTYPE);
//Your Domain name with URL path or IP address with path
const char* serverName = "http://192.168.220.190:5000/sensordata/";
unsigned long lastTime = 0;
unsigned long timerDelay = 5000;

void setup() {
  Serial.begin(115200);
  pinMode(Buzzer, OUTPUT); 
  dht.begin();  
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");
}

void loop() {
    int gassensorAnalog = analogRead(Gas_analog);
    int firesensorAnalog = analogRead(Fire_analog);
  if ((millis() - lastTime) > timerDelay) {
    if(WiFi.status()== WL_CONNECTED){
      WiFiClient client;
      HTTPClient http;    
      http.begin(client, serverName);

    //reading sensor data

      float h = dht.readHumidity();
      float t = dht.readTemperature();
      float hic = dht.computeHeatIndex(t, h, false);
      if(t>32 || firesensorAnalog<3500){
        alert=1;
        digitalWrite(Buzzer,HIGH);
      }
      else{
        alert=0;
        digitalWrite(Buzzer,LOW);

      }


    //posting sensor data
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      String httpRequestData = "mongoid="+mongoid+
                                "&fire="+String(firesensorAnalog)+
                                "&gas="+String(gassensorAnalog)+
                                "&temp="+String(t)+
                                "&humidity="+String(h)+
                                "&alert="+String(alert);
      int httpResponseCode = http.POST(httpRequestData);
      Serial.println(httpRequestData);
      Serial.print("HTTP Response code: ");
      //Serial.println(httpResponseCode);
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}