#!/usr/bin/env python3
import discord
from discord.ext import commands
import sys
import os


if os.environ.get('GOLIVE_BOT_PREFIX'):
    command_prefix = os.environ.get('GOLIVE_BOT_PREFIX')
else:
    command_prefix = "gl."

if os.environ.get('GOLIVE_BOT_TOKEN'):
    bot_token = os.environ.get('GOLIVE_BOT_TOKEN')
else:
    sys.exit("please set GOLIVE_BOT_TOKEN env var to your bot token")

owner_list = []


bot = commands.Bot(command_prefix=command_prefix)


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
            print(f"Added {team_member.name} to owner list")
    else:
        owner_list.append(int(app_info.owner.id))
        print(f"Added {app_info.owner.name} to owner list")

    print("------")
    print(f"Use this command prefix: {command_prefix}")
    print(f"Available commands:")
    print(f"{command_prefix}join <channel_id>")
    print(f"{command_prefix}leave")
    print(f"------")


@bot.command()
async def leave(ctx):
    if not int(ctx.author.id) in owner_list:
        return
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()
    await ctx.message.add_reaction("✅")


@bot.command()
async def join(ctx, channel_id):
    if not int(ctx.author.id) in owner_list:
        return

    target_channel = bot.get_channel(int(channel_id))
    if not target_channel:
        print("can't find a channel with that ID")
        return
    await target_channel.connect()

    # ffmpeg -f pulse -i default
    audio_source = discord.FFmpegPCMAudio("default", before_options="-f pulse", options="")
    ctx.voice_client.play(audio_source)
    await ctx.message.add_reaction("✅")


bot.run(bot_token)
