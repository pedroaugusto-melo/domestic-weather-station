# Estação Climática Doméstica - Back-end

## Descrição

Neste arquivo, serão detalhadas as configurações do servidor MQTT e do back-end da plataforma web que será construída no projeto.

## Configuração

Para configurar esta parte da estação climática domética, siga os passos abaixo.

### 1. Configuração do broker MQTT

Como broker MQTT, será utilizado o `mosquitto`, o qual é uma ferramenta open-source. Para instalá-lo em sistemas Debian/Ubuntu, use:

```
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
```

O arquivo de configuração do `mosquitto` normalmente está no seguinte endereço: `/etc/mosquitto/mosquitto.conf`. No diretório do arquivo de configuração, será criado um arquivo de senhas. Para isso, use:

```
sudo mosquitto_passwd -c /etc/mosquitto/passwd NOME_USUARIO
```

No lugar de `NOME_USUARIO`, escolha um nome que será utilizado para autenticação. Assim que o comando acima for digitado, será pedida uma senha. Esse usuário e essa senha serão utilizados pelo hardware do projeto, confome descrito [aqui](../hardware/README.md#2-configuração-do-servidor-mqtt).

Posteriormente, edite o arquivo de configuração do `mosquitto` para incluir o arquivo de senha e solicitar a autenticação dos usuários conectados ao broker. Para abrir tal arquivo, use:

```
sudo nano /etc/mosquitto/mosquitto.conf
```

No arquivo de configuração, adicione as seguintes linhas:

```
allow_anonymous false
password_file /etc/mosquitto/passwd
```

Nesse arquivo, também está declarada a porta de comunicação utilizada pelo broker. Essa informação será utilizada pelo hardware, confome descrito [aqui](../hardware/README.md#2-configuração-do-servidor-mqtt).

Reinicie o broker, usando:

```
sudo service mosquitto restart
```

**Observações:**

1. Comandos úteis relativos ao broker `mosquitto`:

- Inicialização: `sudo service mosquitto start`

- Interrompimento: `sudo service mosquitto stop`

- Reinicialização: `sudo service mosquitto restart`

2. Para que o harware consiga se comunicar com o broker, o endereço do broker de IP do broker deve ser inserido no arquivo do hardware, conforme especificado [aqui](../hardware/README.md#configuração).

### 2. Configuração do back-end

Para configurar o back-end do projeto, siga os passos abaixo.

#### 2.1. Criação do banco de dados

Inicialmente, crie um banco de dados `postgresql` vazio.

#### 2.2. Configuração das variáveis de ambiente

Posteriormente, na raiz do repositório deste projeto (`../`), crie um arquivo `.env` com as seguintes variáveis:

```
DOMAIN=localhost

# Used by the backend to generate links in emails to the frontend
FRONTEND_HOST=http://localhost:5173

# Environment: local, staging, production
ENVIRONMENT=local
PROJECT_NAME="Domestic Weather Station"
STACK_NAME=full-stack-fastapi-project

# Backend
BACKEND_CORS_ORIGINS="http://localhost,http://localhost:5173,https://localhost,https://localhost:5173,http://localhost.tiangolo.com"
SECRET_KEY=ba79b82a79c9ad4327bdfbc7b872ac244bba1e5427d0236d1f2d4da26f7cea759975a8b4959ac9915424da816ac1e6b5d613ccb160ebc9dcc566c6edbbbae516e15877e491e343ed474d27df977c1ba6a0b174dd10a604b971b855fe9bc6915d499e0e3628526c7fd51c3211749b2f28104655b5974257229f797b1fb68b2bbf52d6eb350418529de5e52a9922976eee6f77bf6de9e56aa09abbfdd7247dc8571379c9fb41f51cc247c3e03af1a8e614d7977925a39d733bfc3e1d7c8eb574c48488b1d95ba74fcd21bd0442e3a198b2123b952d482d8b99630dfb86bd0fb49191255da5d790a8a0f1e7002ea221f845ec7fede34d597b36d14a8d98b9abbf0f
FIRST_SUPERUSER=admin@dws.com
FIRST_SUPERUSER_PASSWORD=teste123

# MQTT
MQTT_BROKER_HOST=
MQTT_BROKER_PORT=
MQTT_BROKER_USERNAME=
MQTT_BROKER_PASSWORD=

# Emails
SMTP_HOST=
SMTP_USER=
SMTP_PASSWORD=
EMAILS_FROM_EMAIL=
SMTP_TLS=
SMTP_SSL=
SMTP_PORT=

# Postgres
POSTGRES_SERVER=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

Na arquivo acima, na seção `MQTT`, preencha com as variáveis configuradas no broker, [conforme especificado anteriormente](./README.md#1-configuração-do-broker-mqtt).
Na seção `Emails`, caso queira usar as features do back-end que envolvem envio de emails, preencha os valores das variáveis. Tal seção é opcional.
Por fim, na seção `Postgres`, preencha os dados relativos ao banco de dados `postgresql`.

#### 2.3. Instalação das dependendências do back-end

Para instalar as dependências, primeiro crie, neste diretório, um ambiente virtual python:

```
python3.12 -m venv .venv
```

Em seguida, instale as dependências:

```
pip install .
```

#### 2.4. Atualização e inicialização do banco de dados

Para criar as tabelas do projeto no banco de dados e preenchê-las com os dados iniciais, execute, neste diretório, o seguinte comando:

```
bash scripts/pre-start.sh
```

#### 2.5. Inicialização da API

Para inicializar o back-end, utilize, neste diretório, o comando abaixo:

```
uvicorn app.main:app --reload
```
