# src/interface/slack_bot.py

import os
import sys
from dotenv import load_dotenv
from slack_sdk import WebClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from src.core.chain_orchestrator import orchestrate_project

# Load environment variables
load_dotenv()
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
print(client.auth_test())

# Initialize Slack app
app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)

# Handle all messages
@app.event("message")
def handle_message(event, say):
    user_input = event.get('text')
    user = event.get('user')

    say(f"🤖 Hey <@{user}>, I'm working on your request...")

    try:
        response = orchestrate_project(user_input)
        say(f"✅ Done! Here's the result:\n```{response}```")
    except Exception as e:
        say(f"❌ Oops! Something went wrong:\n```{str(e)}```")
    print("📥 Slack Event:", event)

if __name__ == "__main__":
    print("🚀 Starting Slack bot...")
    handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    handler.start()



