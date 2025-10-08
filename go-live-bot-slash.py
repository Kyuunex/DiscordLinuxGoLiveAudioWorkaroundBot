#!/usr/bin/env python3
import discord
from discord import app_commands
import sys
import os

from pulseaudio_source import PulseAudioSource

config_dir_path = os.path.join(os.path.expanduser("~"), ".local", "share", "go-live-bot")
token_file_path = os.path.join(config_dir_path, "token.txt")

bot_token = None

if os.path.exists(token_file_path):
    with open(token_file_path, "r+") as token_file:
        bot_token = token_file.read().strip()

if os.environ.get('GOLIVE_BOT_TOKEN'):
    bot_token = os.environ.get('GOLIVE_BOT_TOKEN')

if not bot_token:
    sys.exit("i need the bot token to work. either set GOLIVE_BOT_TOKEN env var or put it in: " + token_file_path)

owner_list = []

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

    app_info = await bot.application_info()
    if app_info.team:
        for team_member in app_info.team.members:
            owner_list.append(int(team_member.id))
            print(f"Added {team_member.name} to the bot operator list")
    else:
        owner_list.append(int(app_info.owner.id))
        print(f"Added {app_info.owner.name} to the bot operator list")

    print("------")
    print("Waiting to finish syncing the slash commands...")
    await tree.sync()
    print("Slash commands synced globally!")
    print(f"Available commands:")
    print(f"/join")
    print(f"/leave")
    print(f"------")


@tree.command(name="leave", description="Leave the VC")
async def leave(ctx: discord.Interaction):
    if int(ctx.user.id) not in owner_list:
        return
    ctx.guild.voice_client.stop()
    await ctx.guild.voice_client.disconnect()
    await ctx.response.send_message(":ok_hand:")


@tree.command(name="join", description="Join the VC")
async def join(ctx: discord.Interaction):
    if not int(ctx.user.id) in owner_list:
        return

    if ctx.guild.voice_client and ctx.guild.voice_client.is_playing():
        ctx.guild.voice_client.stop()
        await ctx.guild.voice_client.disconnect()

    if type(ctx.channel) != discord.VoiceChannel:
        await ctx.response.send_message("type the command in a voice channel you wish me to join")
        return

    target_channel = ctx.channel

    await target_channel.connect()

    for voice_client in bot.voice_clients:
        if voice_client.channel == target_channel:
            audio_source = PulseAudioSource()

            voice_client.play(
                audio_source,
                application="lowdelay"
            )

    await ctx.response.send_message(f"Joined {target_channel.mention}!")


bot.run(bot_token)
