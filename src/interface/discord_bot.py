# src/interface/discord_bot.py

import discord
import os
import sys
from dotenv import load_dotenv

# ✅ Setup path to import your project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.agents.planner_agent import generate_plan
from src.agents.writer_agent import write_code
from src.agents.test_agent import generate_tests
from src.agents.doc_agent import generate_readme_and_gitignore
from src.agents.docker_agent import generate_dockerfile

# ✅ Load Discord bot token from .env
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Add this to your .env file

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot is running as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_input = message.content.strip()

    if user_input.startswith("!plan"):
        idea = user_input[6:]
        await message.channel.send("🧠 Generating project plan...")
        plan = generate_plan(idea)
        await message.channel.send(f"📋 Plan:\n{plan}")

    elif user_input.startswith("!write"):
        idea = user_input[7:]
        await message.channel.send("✍️ Writing code...")
        result = write_code(idea)
        await message.channel.send(f"📦 Code:\n```python\n{result}\n```")

    elif user_input.startswith("!test"):
        idea = user_input[6:]
        await message.channel.send("🧪 Generating tests...")
        result = generate_tests(idea)
        await message.channel.send(f"🧾 Tests:\n```python\n{result}\n```")

    elif user_input.startswith("!docs"):
        idea = user_input[6:]
        await message.channel.send("📄 Creating README and .gitignore...")
        docs = generate_readme_and_gitignore(idea)
        await message.channel.send(f"📘 README:\n{docs['README.md']}\n\n🚫 .gitignore:\n{docs['.gitignore']}")

    elif user_input.startswith("!docker"):
        idea = user_input[8:]
        await message.channel.send("🐳 Creating Dockerfile...")
        dockerfile = generate_dockerfile(idea)
        await message.channel.send(f"🐋 Dockerfile:\n```Dockerfile\n{dockerfile}\n```")

    elif user_input.startswith("!help"):
        help_text = """
🤖 **AutoCode-GPT-X Bot Commands**:
- `!plan <idea>` → Generate project plan
- `!write <idea>` → Generate starter code
- `!test <idea>` → Generate test cases
- `!docs <idea>` → Create README and .gitignore
- `!docker <idea>` → Generate Dockerfile
- `!help` → Show this message
"""
        await message.channel.send(help_text)

client.run(DISCORD_TOKEN)


