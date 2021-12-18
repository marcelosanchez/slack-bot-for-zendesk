import json

import slack
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Slack:
    def __init__(self):
        self.tocken = os.environ['SLACK_BOT_TOKEN']

    def send_messange_to_slack_channel(self, channel_name, message, json_block_msg):
        client = slack.WebClient(token=self.tocken)
        client.chat_postMessage(channel='#' + channel_name, text=message, blocks=json.dumps(json_block_msg))
        print("Mensaje enviado - #" + channel_name)
