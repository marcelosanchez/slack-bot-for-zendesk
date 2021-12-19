# slack-bot-zd
Bot de Slack para notificar tickets de Zendesk

1. Instalar las dependencias.
```
pip install -r requirements.txt
```

2. Iniciar el bot.
```
python mr_zen_bot.py
```

### Observaciones:
Es necesario crear un archivo `.env` con la siguiente información (reemplazar `XXXXX` por su información real):
```
SLACK_APP_TOKEN=XXXXX
SLACK_BOT_TOKEN=XXXXX
SIGNING_SECRET=XXXXX
BOT_CHANNEL=nombre_canal
```
Se debe crear un canal en Slack e invitar al bot `MrZen Bot`, para poder recibir los mensajes.

Es necesario crear un archivo `creds_zendesk.json` con la siguiente información: 
```
{
    "email": "miemail@dezendesk.com",
    "password": "mI_c0ntrasenIa",
    "subdomain": "misubdominio"
}
```
Para las claves de autenticacion, es necesario que se generen en el Api de Zendesk.