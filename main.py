import os
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message, app_commands
from discord.ext import commands, tasks
from responses import get_response

# load token
load_dotenv()
bot_token = os.getenv('bot_token')

# bot setup
intents: Intents = Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Message Empty')
        return
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# bot startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is awake!')

    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command/s")
    except Exception as e:
        print(e)


@client.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello {interaction.user.mention}, You\'re a true one')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: {user_message}')
    await send_message(message, user_message)

def main() -> None:
    client.run(token=bot_token)


if __name__ == '__main__':
    main()