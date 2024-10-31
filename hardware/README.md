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

## Análise de adição de novos sensores

1. Sensores usados atualmente:
   1."DHT22": sensor de temperatura e de umidade do ar;
   2."MQ-135": sensor de gases tóxicos.

2. Sensor "DHT22"

   1. A princípio, seria possível usar o sensor DHT11 para medir temperatura e umidade. Contudo isso não será feito pelas seguintes razões:
      1. O grupo já dispõe de um DHT22;
      2. O sensor DHT22 apresenta desempenho superior ao do sensor DHT11: o DHT11 e o DHT22 funcionam bem para intervalos de umidade, respectivamente, de 20% a 80% e de 0% a 100%;
   2. O DHT22 é um tanto lento (tempo mínimo entre medições consecutivas: 2 segundos). Porém isso não faz diferença para a aplicação proposta;
   3. Não vejo sentido em trocar o DHT22. Por isso, o melhor e manter esse sensor de temperatura e umidade.

3. Microcontrolador usado: "ESP-32"

4. Sensor "MQ-135"

   1. Sensor de gases tóxicos/nocivos;
   2. Seu principal alvo é o CO2, mas também é capaz de detectar:
      1. Compostos orgânicos voláteis;
      2. Óxidos de nitrogênio (NOx);
      3. Vapor de etanol;
      4. Fumaça;
      5. Amônia;
   3. Necessita de pré-aquecimento antes de poder fornecer resultados acurados;
   4. Material ativo: SnO2 (óxido de estanho)
   5. Defeitos:
      1. Caso seja exposto a altas concentrações de gases corrosivos (Cl2, NH3, H2S, SO2), deixa rapidamente de funcionar. Portanto, **não pode ser usado para a detecção de compostos de halogênios ou de enxofre**;
      2. Altamente suscetível a dano por compostos voláteis de silício. Dessa forma, pode ser problemático usá-lo próximo a silicones;
      3. Não é um bom sensor para gases nocivos com enxofre (H2S, SO2, etc...);

5. Outros possíveis gases nocivos a detectar:
   1. Vapor de Hg (não achei nenhum sensor que meça especificamente isso);
   2. Ozônio (candidato promissor: [MQ-131](https://jxctgas.com/product/5605?utm_source=Google%20Shopping&utm_campaign=jxctgas&utm_medium=cpc&utm_term=5383&srsltid=AfmBOoqFbOY-BDIgkuXO6pkAGrfySbw5lRuB9J1SkhT5vf50Gz3K0wQB-jc));
   3. Óxidos de enxofre (sensores de dióxido de enxofre parecem ser extremamente caros);
   4. H2S (candidato promissor: [MQ-136](https://www.usinainfo.com.br/sensor-de-gas-arduino/detector-de-gas-sensor-de-gas-mq-136-gas-sulfidrico-h2s-4601.html));
