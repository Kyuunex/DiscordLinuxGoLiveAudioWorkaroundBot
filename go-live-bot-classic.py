#!/usr/bin/env python3
import discord
from discord.ext import commands
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

if os.environ.get('GOLIVE_BOT_PREFIX'):
    command_prefix = os.environ.get('GOLIVE_BOT_PREFIX')
else:
    command_prefix = "gl."

owner_list = []

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix=command_prefix)


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
    print(f"Use this command prefix: {command_prefix}")
    print(f"Available commands:")
    print(f"{command_prefix}join")
    print(f"{command_prefix}leave")
    print(f"------")


@bot.command()
@commands.guild_only()
async def leave(ctx):
    if not int(ctx.author.id) in owner_list:
        return
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()
    try:
        await ctx.reply(":ok_hand:")
    except discord.Forbidden:
        print("channel left")


@bot.command()
@commands.guild_only()
async def join(ctx):
    if not int(ctx.author.id) in owner_list:
        return

    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()

    if type(ctx.channel) != discord.VoiceChannel:
        await ctx.reply("type the command in a voice channel you wish me to join")
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

            await ctx.reply(f"joined {target_channel.mention}")


bot.run(bot_token)
