import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import httpx

load_dotenv()

TOKEN = 'Your Bot Token'
PANEL_URL = 'Your Panel URL'
API_KEY = 'Your Panel API Key'
BOT_OWNER_ID = 'Bot Owner ID'

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

client = httpx.Client(base_url=PANEL_URL, headers={'Authorization': f'Bearer {API_KEY}'})

admins = set()

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    print('Bot is ready!')

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
    response = "Here are the available servers:\n"
    try:
        res = await client.get('/api/application/servers')
        res.raise_for_status()
        servers = res.json()
        for server in servers['data']:
            response += f"{server['attributes']['identifier']}: {server['attributes']['name']}\n"
        await ctx.send(response)
    except httpx.HTTPError as e:
        await ctx.send(f"Error listing servers: {str(e)}")

@bot.command(name='restart')
@is_bot_owner_or_admin()
async def restart_server(ctx, server_id: str):
    try:
        res = await client.post(f'/api/application/servers/{server_id}/power', json={'signal': 'restart'})
        res.raise_for_status()
        await ctx.send(f"Server with ID '{server_id}' has been restarted.")
    except httpx.HTTPError as e:
        await ctx.send(f"Error restarting server: {str(e)}")

@bot.command(name='start')
@is_bot_owner_or_admin()
async def start_server(ctx, server_id: str):
    try:
        res = await client.post(f'/api/application/servers/{server_id}/power', json={'signal': 'start'})
        res.raise_for_status()
        await ctx.send(f"Server with ID '{server_id}' has been started.")
    except httpx.HTTPError as e:
        await ctx.send(f"Error starting server: {str(e)}")

@bot.command(name='stop')
@is_bot_owner_or_admin()
async def stop_server(ctx, server_id: str):
    try:
        res = await client.post(f'/api/application/servers/{server_id}/power', json={'signal': 'stop'})
        res.raise_for_status()
        await ctx.send(f"Server with ID '{server_id}' has been stopped.")
    except httpx.HTTPError as e:
        await ctx.send(f"Error stopping server: {str(e)}")

@bot.command(name='status')
@is_bot_owner_or_admin()
async def server_status(ctx, server_id: str):
    try:
        res = await client.get(f'/api/application/servers/{server_id}')
        res.raise_for_status()
        server = res.json()
        status = server['attributes']['status']
        await ctx.send(f"Server with ID '{server_id}' is {status}.")
    except httpx.HTTPError as e:
        await ctx.send(f"Error getting server status: {str(e)}")

@bot.command(name='usage')
@is_bot_owner_or_admin()
async def server_usage(ctx, server_id: str):
    try:
        res = await client.get(f'/api/application/servers/{server_id}/utilization')
        res.raise_for_status()
        usage = res.json()['attributes']
        cpu = usage['cpu_absolute']
        memory = usage['memory_bytes']
        disk = usage['disk_bytes']
        await ctx.send(f"CPU usage: {cpu}\nMemory usage: {memory}\nDisk usage: {disk}")
    except httpx.HTTPError as e:
        await ctx.send(f"Error getting server usage: {str(e)}")

@bot.command(name='stats')
@is_bot_owner_or_admin()
async def panel_stats(ctx):
    try:
        res_nodes = await client.get('/api/application/nodes')
        res_nodes.raise_for_status()
        nodes = res_nodes.json()['data']

        res_servers = await client.get('/api/application/servers')
        res_servers.raise_for_status()
        servers = res_servers.json()['data']

        res_users = await client.get('/api/application/users')
        res_users.raise_for_status()
        users = res_users.json()['data']

        response = f"**Pterodactyl Panel Stats**\nNodes: {len(nodes)}\nServers: {len(servers)}\nUsers: {len(users)}"
        await ctx.send(response)
    except httpx.HTTPError as e:
        print(e)
        await ctx.send(f"Error getting panel stats: {str(e)}")

bot.run(TOKEN)
