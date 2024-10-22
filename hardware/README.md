# Estação Climática Doméstica - Hardware

## Descrição

A principal função do hardware deste projeto é coletar dados, por meio de sensores, e enviá-los, via protocolo MQTT (mais detalhes dessa forma de comunicação podem ser encontradas [aqui](https://mqtt.org/)), para um broker. Tais dados são agrupados em tópicos. No nosso caso, são quatro: `temperature/domestic_weather_station`, `humidity/domestic_weather_station`, `heat_index/domestic_weather_station`, `gas_level/domestic_weather_station`.

O broker redireciona esses dados para os serviços que estiverem "ouvindo" informações específicas de um certo tópico. No nosso caso, esse "ouvinte" é o back-end, o qual está inscrito nos quatro tópicos.

## Configuração

Para usar o harware da estação climática doméstica, siga os passos abaixo.

### 1. Configurações do WiFi

Para que o microcontrolador ESP-32 consiga se conectar na internet, é necessário utilizar uma rede WiFi. O nome e a senha dessa rede devem ser definidos nas variáveis `SSID` e `SSID_PASSWORD`, respectivamente, do arquivo `main.ino`, localizado neste diretório.

### 2. Configuração do servidor MQTT

Os dados coletados pelos sensores da estação serão enviados, utilizando o protocolo de comunicação MQTT, para um broker, o qual é um servidor intermediário que recebe os dados de fontes (`publishers`) - no nosso caso, o hardware da estação climática - e envia para ouvintes (`subscribers`) - no nosso caso, o servidor back-end. Assim, para que o ESP-32 se comunique com o broker, as seguintes variáveis, no arquivo `main.ino`, neste diretório, devem ser configuradas:

- `MQTT_SERVER`: endereço do broker
- `MQTT_SERVER_PORT`: porta no broker habilitada para a comunicação MQTT
- `MQTT_SERVER_USER`: usuário do broker
- `MQTT_SERVER_PASSWORD`: senha do usuário do broker
