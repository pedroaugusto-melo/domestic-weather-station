#include "DHT.h"
#include <WiFi.h>
#include <PubSubClient.h>

#define TEMP_HUM_PIN 32
#define GAS_PIN 34  

#define DHT_TYPE DHT22

#define SSID ""
#define SSID_PASSWORD ""

#define MQTT_SERVER ""
#define MQTT_SERVER_PORT 1883
#define MQTT_SERVER_USER ""
#define MQTT_SERVER_PASSWORD ""


DHT dht(TEMP_HUM_PIN, DHT_TYPE);

WiFiClient espClient;
PubSubClient client(espClient);

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

void publishTempData() {
  String payload = "{";
  payload += "\"temperature\":";
  payload += temperature;
  payload += "}";

  client.publish("temperature/domestic_weather_station", payload.c_str());
}

void publishHumidityData() {
  String payload = "{";
  payload += "\"humidity\":";
  payload += humidity;
  payload += "}";

  client.publish("humidity/domestic_weather_station", payload.c_str());
}

void publishHeatIndexData() {
  String payload = "{";
  payload += "\"heat_index\":";
  payload += heatIndex;
  payload += "}";

  client.publish("heat_index/domestic_weather_station", payload.c_str());
}

void publishGasLevelData() {
  String payload = "{";
  payload += "\"gas_level\":";
  payload += gasLevel;
  payload += "}";

  client.publish("gas_level/domestic_weather_station", payload.c_str());
}

// --------------------------------------------------------------------

void setup() {
  setupSerial();
  Serial.println("Initializing system...");
  
  setupWiFi();
  setupESPClient();
  dht.begin();
  
  delay(2000);
  Serial.println("Initializing lectures...");
}

void loop() {
  connectMQTT();

  readTempHumData();
  readGasData();

  publishTempData();
  publishHumidityData();
  publishHeatIndexData();
  publishGasLevelData();
  Serial.println("(Data published)");

  Serial.print("\n");
  
  delay(2000);
}
