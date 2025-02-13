import discord
from discord import app_commands
from src.database import TagDatabase
from src.commands import TagCommands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def main():
    db = TagDatabase()
    tag_commands = TagCommands(db, client)
    tag_commands.setup_commands(tree)

    @client.event
    async def on_ready():
        await tree.sync()
        print(f"Logged in as {client.user}")

    try:
        with open("token.txt", "r") as f:
            token = f.read().strip()
        client.run(token)
    except FileNotFoundError:
        print("Create a 'token.txt' file containing your bot token")

if __name__ == "__main__":
    main()