import logging
import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.INFO)
load_dotenv()

#testsocket = xapp-1-A05KKB7BZRT-5653773189607-4056787bdbedb88b102fb612be5de9bd743650273cea3b984f6c04a764bf350f
#testauth = xoxb-5665375267509-5665439564245-B6Dm1i2Sqi9sDrAostS2Uzvq

SLACK_BOT_TOKEN = os.environ["user_oauth_token"] 
SLACK_APP_TOKEN = os.environ["socket_mode_token"]

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def mention_handler(body, say):
    say("Hello World")

@app.event("message")
def message_hander(body):
    pass

if __name__ == "__main__":
    if hasattr(app.client, "proxy"):
        handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    else:
        handler = SocketModeHandler(app, SLACK_APP_TOKEN, proxy=None)

handler.start()