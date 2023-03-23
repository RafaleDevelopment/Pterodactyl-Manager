<h1>Pterodactyl-Manager</h1>
Pterodactyl-manager simplifies the management of Pterodactyl panel in Discord servers which allows host owners to manage tasks easily.

<h2>About Pterodactyl-Manager</h2>

<p>A Discord bot developed by Rafale Development makes it easier to handle Pterodactyl game servers. This bot is ideal for server administrators and owners that require a quick way to handle activities like starting, pausing, restarting, checking the status of the server, and tracking usage.

The bot was created specifically for servers that use Pterodactyl as their game server management panel. It uses both the Discord API and Pterodactyl API client. Since our bot is distributed under the permissive MIT licence, users are allowed to alter and personalise it as they see fit.

Open an issue on this repository if you have any questions, bug reports, or feature requests.</p>

<h2>Support</h2>

<p>If you need any support regarding our bot you can freely contact us in our 
discord server https://discord.gg/KXAwSr43CZ</p>

<h2>Bot Features</h2>

Start server<br>
Stop server<br>
Restart seever<br>
List server<br>
Show server status<br>
Show server usage<br>
Add admin & Remove admin <em>(For bot)</em><br>

<h2>Required Packages</h2>

<strong>Make Sure To Install These Packages To Run The Bot Else It Will Not Work</strong>


```pip install discord.py```

```pip install pterodactyl.py```

<h2>Bot Code</h2>

```import os
import discord
from discord.ext import commands
from pterodactyl import PterodactylClient

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
PANEL_URL = os.getenv('PANEL_URL')
API_KEY = os.getenv('PANEL_API_KEY')
BOT_OWNER_ID = int(os.getenv('BOT_OWNER_ID'))

bot = commands.Bot(command_prefix='!')
client = PterodactylClient(PANEL_URL, API_KEY)

admins = set()

def is_bot_owner_or_admin():
    async def predicate(ctx):
        return ctx.author.id == BOT_OWNER_ID or ctx.author.id in admins
    return commands.check(predicate)

@bot.command(name='credits')
async def credits(ctx):
    response = "This bot was made by Rafale Development."
    await ctx.send(response)

@bot.command(name='add_admin')
@commands.is_owner()
async def add_admin(ctx, user_id: int):
    admins.add(user_id)
    await ctx.send(f"User with ID '{user_id}' has been added as an admin.")

@bot.command(name='remove_admin')
@commands.is_owner()
async def remove_admin(ctx, user_id: int):
    admins.discard(user_id)
    await ctx.send(f"User with ID '{user_id}' has been removed as an admin.")

@bot.command(name='servers')
@is_bot_owner_or_admin()
async def list_servers(ctx):
    servers = client.servers.list_servers()
    response = "Here are the available servers:\n"
    for server in servers:
        response += f"{server.id}: {server.name}\n"
    await ctx.send(response)

@bot.command(name='restart')
@is_bot_owner_or_admin()
async def restart_server(ctx, server_id: str):
    try:
        client.servers.restart_server(server_id)
        await ctx.send(f"Server with ID '{server_id}' has been restarted.")
    except Exception as e:
        await ctx.send(f"Error restarting server: {str(e)}")

@bot.command(name='start')
@is_bot_owner_or_admin()
async def start_server(ctx, server_id: str):
    try:
        client.servers.start_server(server_id)
        await ctx.send(f"Server with ID '{server_id}' has been started.")
    except Exception as e:
        await ctx.send(f"Error starting server: {str(e)}")

@bot.command(name='stop')
@is_bot_owner_or_admin()
async def stop_server(ctx, server_id: str):
    try:
        client.servers.stop_server(server_id)
        await ctx.send(f"Server with ID '{server_id}' has been stopped.")
    except Exception as e:
        await ctx.send(f"Error stopping server: {str(e)}")

@bot.command(name='status')
@is_bot_owner_or_admin()
async def server_status(ctx, server_id: str):
    try:
        server = client.servers.get_server(server_id)
        status = server.status
        await ctx.send(f"Server with ID '{server_id}' is {status}.")
    except Exception as e:
        await ctx.send(f"Error getting server status: {str(e)}")

@bot.command(name='usage')
@is_bot_owner_or_admin()
async def server_usage(ctx, server_id: str):
    try:
        usage = client.servers.get_server_utilization(server_id)
        cpu = usage.cpu
        memory = usage.memory
        disk = usage.disk
        response = f"Server with ID '{server_id}' utilization:\n"
        response += f"CPU: {cpu}%\nMemory: {memory} MB\nDisk: {disk} MB"
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error getting server usage: {str(e)}")

bot.run(TOKEN)```



