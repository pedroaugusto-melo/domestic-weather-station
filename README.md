# Estação climática doméstica - Overview

## Introdução

O objetivo deste projeto é desenvolver o protótipo de um produto que seja passível de comercialização e que se relacione com boas práticas ambientais. Tal desenvolvimento contemplará tanto a parte de hardware quando a parte de software do produto.

Nesse sentido, foi escolhido desenvolver uma estação climática doméstica, a qual será capaz de fornecer dados e _insights_ totalmente personalizados. O escopo dessas informações oferecidas pela estação será direcionado, principalmente, para aspectos de saúde, de bem-estar e de segurança.

Inicialmente, os dados medidos pela estação climática doméstica serão: temperatura, umidade do ar, sensação térmica e nível de gases tóxicos. Espera-se, ao final do projeto, ter uma plataforma web que não só exiba esses dados como também, por meio de ferramentas de inteligência artifical, forneça _insights_ sobre eles. Como exemplo desses _insights_, pode-se citar sugestões de práticas que promovam o bem estar respiratório em cenários de ar seco, alerta de incêndios em cenários de elevado nível de gases tóxicos, entre outros.

## Arquitetura do produto

![Arquitetura do produto](./img/architecture.png)

Mais detalhes sobre a configuração do servidor MQTT e do back-end da plataforma podem ser encontrados [aqui](./backend/README.md).

## Hardware do produto

![Hardware do produto](./img/station_hardware.jpg)

Componentes:

- Microcontrolador ESP-32
- Sensor de temperatura e umidade (DHT22)
- Sensor de gases tóxicos (MQ-135)

Mais detalhes sobre a configuração do hardware podem ser encontrados [aqui](./hardware/README.md).

## Modelagem dos dados do produto

![Modelagem dos dados](./img/data_modeling.png)

Nessa modelagem, as principais entidades são:

- `user`: usuário que possui uma estação climática ou que é um administrador do sistema
- `microcontroller`: microcontrolador que pode ser usado em uma estação climática
- `sensor`: sensor que pode ser usado em uma estação climática
- `weather_station_model`: modelo de estação climática, o qual define, basicamente, o microcontrolador (`microcontroller`) e os sensores (`sensor`) que uma estação climática possui
- `weather_station`: estação climática concreta, caracterizada por um certo modelo (`weather_station_model`) e pertencente a um certo usuário (`user`)
- `temperature_reading`: leituras de temperatura feitas por um certo sensor (`sensor`) em uma certa estação climática (`weather_station`)
- `gas_level_reading`: leituras de nível de gases tóxicos feitas por um certo sensor (`sensor`) em uma certa estação climática (`weather_station`)
- `humidity_reading`: leituras de umidade relativa do ar feitas por um certo sensor (`sensor`) em uma certa estação climática (`weather_station`)
- `heat_index_reading`: leituras de sensação térmica feitas por um certo sensor (`sensor`) em uma certa estação climática (`weather_station`)
