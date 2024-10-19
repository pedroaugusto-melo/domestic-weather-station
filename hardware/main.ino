#include <NTPClient.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <PubSubClient.h>
#include "DHT.h"

#define TEMP_HUM_PIN 32
#define GAS_PIN 34  

#define DHT_TYPE DHT22

#define DHT22_SENSOR_PART_NUMBER 1
#define MQ135_SENSOR_PART_NUMBER 2
#define STATION_PART_NUMBER 1

#define SSID ""
#define SSID_PASSWORD ""

#define MQTT_SERVER ""
#define MQTT_SERVER_PORT 1883
#define MQTT_SERVER_USER ""
#define MQTT_SERVER_PASSWORD ""


DHT dht(TEMP_HUM_PIN, DHT_TYPE);

WiFiClient espClient;
PubSubClient client(espClient);

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 0, 60000);

float temperature;
float humidity;
float heatIndex;
int gasLevel;

// --------------------------------------------------------------------

void setupSerial() {
  Serial.begin(9600);
}

void setupESPClient() {
  client.setServer(MQTT_SERVER, MQTT_SERVER_PORT);
}

void setupWiFi() {
  delay(10);

  Serial.println("Initializing WiFi...");

  WiFi.begin(SSID, SSID_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
  }

  Serial.print("\n");
  Serial.print("Connected to ");
  Serial.println(SSID);
}

void setupWiFiUDP() {
  timeClient.begin();

  while(!timeClient.update()){
    timeClient.forceUpdate();
  }
}

void reconnectMQTT() {
  while(!client.connected()) {
    Serial.println("Connecting to MQTT broker...");

    if (client.connect("ESP32Client", MQTT_SERVER_USER, MQTT_SERVER_PASSWORD)) {
      Serial.println("Connected to MQTT broker");
    } else {
      Serial.print("Conexion error:");
      Serial.println(client.state());
      Serial.println("Trying to reconnect in 5s ....");
      delay(5000);
    }
  }
}

void connectMQTT() {
  if (!client.connected()) {
    reconnectMQTT();
  }

  client.loop();
}

void readTempHumData() {
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  heatIndex = dht.computeHeatIndex(temperature, humidity, false);

  Serial.print(F("Humidity: "));
  Serial.print(humidity);
  Serial.print(F("%  Temperature: "));
  Serial.print(temperature);
  Serial.print(F("°C "));
  Serial.print(F("  Heat index: "));
  Serial.print(heatIndex);
  Serial.println(F("°C"));
}

void readGasData() {
  gasLevel = analogRead(GAS_PIN);
  Serial.print("Gas level: ");
  Serial.println(gasLevel);
}

char* getCurrentTimeString(){
  time_t now = timeClient.getEpochTime();
  struct tm* timeInfo = localtime(&now);
  static char timeString[25];
  strftime(timeString, sizeof(timeString), "%Y-%m-%dT%H:%M:%SZ", timeInfo);

  return timeString;
}

const char* getPublishPayload(String measurementType, float measurementValue, int sensorPartNumber) {
  char* currentTimeString = getCurrentTimeString();

  String payload = "{";
  payload += "\"";
  payload += measurementType;
  payload += "\":";
  payload += measurementValue;
  payload += ",";
  payload += "\"read_at\":\"";
  payload += String(currentTimeString);
  payload += "\",";
  payload += "\"sensor_part_number\":\"";
  payload += sensorPartNumber;
  payload += "\",";
  payload += "\"station_part_number\":\"";
  payload += STATION_PART_NUMBER;
  payload += "\"}";

  static String staticPayload;
  staticPayload = payload;
  return staticPayload.c_str();
}

void publishTempData() {
  const char* payload = getPublishPayload("temperature", temperature, DHT22_SENSOR_PART_NUMBER);
  client.publish("temperature/domestic_weather_station", payload);
}

void publishHumidityData() {
  const char* payload = getPublishPayload("humidity", humidity, DHT22_SENSOR_PART_NUMBER);
  client.publish("humidity/domestic_weather_station", payload);
}

void publishHeatIndexData() {
  const char* payload = getPublishPayload("heat_index", heatIndex, DHT22_SENSOR_PART_NUMBER);
  client.publish("heat_index/domestic_weather_station", payload);
}

void publishGasLevelData() {
  const char* payload = getPublishPayload("gas_level", gasLevel, MQ135_SENSOR_PART_NUMBER);
  client.publish("gas_level/domestic_weather_station", payload);
}

// --------------------------------------------------------------------

void setup() {
  setupSerial();
  Serial.println("Initializing system...");
  
  setupWiFi();
  setupWiFiUDP();
  setupESPClient();
  dht.begin();
  
  delay(2000);
  Serial.println("Initializing lectures...");
}

void loop() {
  connectMQTT();

  readTempHumData();
  publishTempData();
  publishHumidityData();
  publishHeatIndexData();
  Serial.println("(DHT22 data published)");

  readGasData();
  publishGasLevelData();
  Serial.println("(MQ135 data published)");

  Serial.print("\n");
  
  delay(2000);
}