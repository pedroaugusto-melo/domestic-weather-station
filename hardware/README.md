# Estação Climática Doméstica - Hardware

## Descrição

A principal função do hardware deste projeto é coletar dados, por meio de sensores, e enviá-los, via protocolo MQTT (mais detalhes dessa forma de comunicação podem ser encontradas [aqui](https://mqtt.org/)), para um broker. Tais dados são agrupados em tópicos. No caso deste projeto, são quatro: `temperature/domestic_weather_station`, `humidity/domestic_weather_station`, `heat_index/domestic_weather_station`, `gas_level/domestic_weather_station`.

O broker envia os dados recebidos para os serviços que estão "ouvindo" informações específicas de um certo tópico. No caso deste projeto, esse "ouvinte" é o back-end, o qual está inscrito (i.e. ouvindo) nos quatro tópicos.

## Configuração

Para configurar o hardware da estação climática doméstica, siga os passos abaixo.

### 1. Configurações do WiFi

Para que o microcontrolador ESP-32 consiga se conectar à internet, é necessário utilizar uma rede WiFi. O nome e a senha dessa rede devem ser definidos nas variáveis `SSID` e `SSID_PASSWORD`, respectivamente, do arquivo `main.ino`, localizado neste diretório.

### 2. Configuração do servidor MQTT

Os dados coletados pelos sensores da estação serão enviados, utilizando o protocolo de comunicação MQTT, para um broker, o qual é um servidor que recebe os dados de fontes (`publishers`) - no caso deste projeto, o hardware da estação climática - e os envia para ouvintes (`subscribers`) - no caso deste projeto, o servidor back-end. Assim, para que o ESP-32 se comunique com o broker, as seguintes variáveis, no arquivo `main.ino`, neste diretório, devem ser configuradas:

- `MQTT_SERVER`: endereço de IP do broker
- `MQTT_SERVER_PORT`: porta do broker habilitada para a comunicação MQTT
- `MQTT_SERVER_USER`: usuário do broker
- `MQTT_SERVER_PASSWORD`: senha do usuário do broker

Mais informações sobre a configuração do broker podem ser encontradas [aqui](../backend/README.md).

### 3. Upload do código no ESP-32

Para gravar o código fonte do arquivo `./main.ino` no ESP-32, pode-se utilizar a [IDE do Arduino](https://www.arduino.cc/en/software/). A fim de se consiga manipular o ESP-32 nessa IDE, algumas configurações extras são necessárias. Mais detalhes sobre isso podem ser encontrados [aqui](https://www.crescerengenharia.com/post/instalando-esp32-arduino).
