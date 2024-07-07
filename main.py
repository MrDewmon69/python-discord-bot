import os
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message, app_commands
from discord.ext import commands, tasks
import requests
import spacy


# load token
load_dotenv()
bot_token = os.getenv('bot_token')
tenor_api = os.getenv('tenor_api')

# bot setup
intents: Intents = Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
nlp = spacy.load("en_core_web_sm")

def get_gif(query):
    url = f"https://api.tenor.com/v1/search?q={query}&key={tenor_api}&limit=1"
    response = requests.get(url)
    try:
        response.raise_for_status()
        data = response.json()
        if 'results' in data and data['results']:
            return data['results'][0]['media'][0]['gif']['url']
        else: 
            print(f"No Gifs found for query: {query}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError as e:
        print(f"JSON decode error: {e}")
    return None

def extract_keywords(text):
    doc = nlp(text)
    keywords = set()
    for enity in doc.ents:
        keywords.add(enity.text)
    for token in doc:
        if token.is_alpha and not token.is_stop:
            keywords.add(token.lemma_)
    return keywords

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
    
    keywords = extract_keywords(message.content.lower())

    for keyword in keywords:
        gif_url = get_gif(keyword)
        if gif_url:
            await message.channel.send(gif_url)
            break


def main() -> None:
    client.run(token=bot_token)


if __name__ == '__main__':
    main()