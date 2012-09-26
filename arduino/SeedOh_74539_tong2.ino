#include <SPI.h>
#include <Ethernet.h>
#include <gLCD.h>
#include "Arduino.h"

#define APIKEY         "h6MsqOTg4cofjLLv8oJE3riBbCaSAKxpVVJTUDlTMVladz0g" // your cosm api key
#define FEEDID         74539 // your feed ID
#define USERAGENT      "Cosm Arduino Example (74539)" // user agent is the project name

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};

IPAddress ip(192,168,0,220);
EthernetClient client;

IPAddress server(216,52,233,121);      // numeric IP for api.cosm.com
//char server[] = "api.cosm.com";   // name address for cosm API

unsigned long lastConnectionTime = 0;          // last time you connected to the server, in milliseconds
boolean lastConnected = false;                 // state of the connection last time through the main loop
const unsigned long postingInterval = 10*1000; //delay between updates to Cosm.com

const char RST = 5;
const char CS = 6;
const char Clk = 8;
const char Data = 7;

#define CDS_PIN A0
#define HUMIDITY_PIN A1
#define LM35_PIN A2
#define SOILMOISTURE_PIN A3

gLCD graphic(RST,CS,Clk,Data,1); //High speed

void setup() {  
 graphic.Init(0,2,0,1,0);
 graphic.Contrast(0x3f); 
 
 // start serial port:
  Serial.begin(9600);
  Serial.println("Go Seed, Oh!");

 Sensor_SetupSoilMoisture();

  draw_temp_humidity();
  draw_light_moisture();
  
 // start the Ethernet connection:
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // DHCP failed, so use a fixed IP address:
    Ethernet.begin(mac, ip);
  }
}

void loop() {
  draw_temp_humidity();
  draw_light_moisture();

  // read the analog sensor:
  int sensorReading = Sensor_GetTemperature();   

  String dataString = "temperature,";
  dataString += sensorReading;

  sensorReading = Sensor_GetHumidity();
  dataString += "\nhumidity,";
  dataString += sensorReading;
  
  sensorReading = Sensor_GetLight();
  dataString += "\nlight,";
  dataString += sensorReading;


  sensorReading = Sensor_GetSoilMoisture();
  dataString += "\nmoisture,";
  dataString += sensorReading;

  // if there's incoming data from the net connection.
  // send it out the serial port.  This is for debugging
  // purposes only:
  if (client.available()) {
    char c = client.read();
    Serial.print(c);
  }

  // if there's no net connection, but there was one last time
  // through the loop, then stop the client:
  if (!client.connected() && lastConnected) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
  }

  // if you're not connected, and ten seconds have passed since
  // your last connection, then connect again and send data: 
  if(!client.connected() && (millis() - lastConnectionTime > postingInterval)) {
    sendData(dataString);
  }
  // store the state of the connection for next time through
  // the loop:
  lastConnected = client.connected();
}

// this method makes a HTTP connection to the server:
void sendData(String thisData) {
  // if there's a successful connection:
  if (client.connect(server, 80)) {
    Serial.println("connecting...");
    // send the HTTP PUT request:
    client.print("PUT /v2/feeds/");
    client.print(FEEDID);
    client.println(".csv HTTP/1.1");
    client.println("Host: api.cosm.com");
    client.print("X-ApiKey: ");
    client.println(APIKEY);
    client.print("User-Agent: ");
    client.println(USERAGENT);
    client.print("Content-Length: ");
    client.println(thisData.length());

    // last pieces of the HTTP PUT request:
    client.println("Content-Type: text/csv");
    client.println("Connection: close");
    client.println();

    // here's the actual content of the PUT request:
    client.println(thisData);
  } 
  else {
    // if you couldn't make a connection:
    Serial.println("connection failed");
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
  }
  // note the time that the connection was made or attempted:
  lastConnectionTime = millis();
}



void draw_temp_humidity() {
  char value_buffer[10];
  
  graphic.SetBackColour(15,15,15);
  graphic.SetForeColour(15,0,0); 
  graphic.Box(0,0,129,129,4);
  
  // TEMP
  graphic.SetForeColour(00,15,0); //Text is coloured Green
  String temp_value = dtostrf(Sensor_GetTemperature(), 2, 0, value_buffer);
  graphic.Print(temp_value,20,50,3); //Normal sized text, no background
  
  graphic.SetBackColour(15,0,15);  
  graphic.Box(0,0,129,65,5);  
  
  /// HUMIDITY
  graphic.SetForeColour(0,0,15); //Text is coloured Blue
  String humidity_value = dtostrf(Sensor_GetHumidity(), 2, 0, value_buffer);
  graphic.Print(humidity_value,20,-10,3); //Normal sized text, no background
  
  // LOADING
  graphic.SetForeColour(10,10,10); //Text is coloured Blue
  for (int j = 0;j <31;j++){
  for (int i = 1;i < 4;i++){
      graphic.Plot((i*4), (j*4),3); //Draw a grid of 16 dots.
    }
    delay(800);    
  } 
}

void draw_light_moisture()
{
  char value_buffer[10];
  
  graphic.SetBackColour(15,15,15);
  graphic.SetForeColour(15,0,0); 
  graphic.Box(0,0,129,129,4);
  
  /// LIGHT
  graphic.SetForeColour(15,0,0); //Text is coloured Red
  String light_value = dtostrf(Sensor_GetLight(), 2, 0, value_buffer);
  graphic.Print(light_value,20,50,3); //Normal sized text, no background
  
  graphic.SetBackColour(15,0,15);  
  graphic.Box(0,0,129,65,5);  
  
  /// MOISTURE
  graphic.SetForeColour(0,0,15); //Text is coloured Blue
  String moisture_value = dtostrf(Sensor_GetSoilMoisture(), 2, 0, value_buffer); 
  graphic.Print(moisture_value,20,-10,3); //Normal sized text, no background
  
  // LOADING
  graphic.SetForeColour(10,10,10); //Text is coloured Blue
  for (int j = 0;j <31;j++){
  for (int i = 1;i < 4;i++){
      graphic.Plot((i*4), (j*4),3); //Draw a grid of 16 dots.
    }
    delay(800);    
  } 
  
}

int Sensor_GetLight() {
  // cds R with lux
  // http://learn.adafruit.com/photocells/using-a-photocell
  int light;
  light = analogRead(CDS_PIN);
  return int(light/ 10);
}

int Sensor_GetTemperature() {
  float temp;
  temp = (5.0 * analogRead(LM35_PIN) * 100.0) / 1024 ;
  return int(temp);
}

int Sensor_GetHumidity() {
  // http://itp.nyu.edu/physcomp/sensors/Reports/ArduinoCode
  int humidityReading = analogRead(HUMIDITY_PIN);
  float humidityVoltage = humidityReading * 5;
  humidityVoltage /= 1024.0;
  float humidityPercentage = humidityVoltage * 100;
  humidityPercentage /= 5;
  return int(humidityPercentage);
}

////////////////////////
#define voltageFlipPin1 2
#define voltageFlipPin2 3

int Sensor_SetupSoilMoisture(){
  pinMode(voltageFlipPin1, OUTPUT);
  pinMode(voltageFlipPin2, OUTPUT);
  pinMode(SOILMOISTURE_PIN, INPUT);
}

void setSensorPolarity(boolean flip){
  if(flip){
    digitalWrite(voltageFlipPin1, HIGH);
    digitalWrite(voltageFlipPin2, LOW);
  }else{
    digitalWrite(voltageFlipPin1, LOW);
    digitalWrite(voltageFlipPin2, HIGH);
  }
}

int Sensor_GetSoilMoisture(){
  int flipTimer = 1000;
  setSensorPolarity(true);
  delay(flipTimer);
  int val1 = analogRead(SOILMOISTURE_PIN);
  delay(flipTimer);  
  setSensorPolarity(false);
  delay(flipTimer);
  // invert the reading
  int val2 = 1023 - analogRead(SOILMOISTURE_PIN);
  //
  return int(val2/10); 
}






