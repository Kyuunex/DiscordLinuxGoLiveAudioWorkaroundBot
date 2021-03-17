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

intents = discord.Intents.default()
intents.members = True
# bot = commands.Bot(command_prefix=command_prefix, intents=intents)
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
    try:
        await ctx.message.add_reaction("✅")
    except:
        print("channel left")


@bot.command()
async def join(ctx, channel_id=None):
    if not int(ctx.author.id) in owner_list:
        return

    target_channel = None

    if channel_id:
        target_channel = bot.get_channel(int(channel_id))
        if not target_channel:
            print("can't find a channel with that ID")
            return
        await target_channel.connect()
    else:
        if ctx.guild:
            if ctx.author.voice:
                target_channel = ctx.author.voice.channel
                await target_channel.connect()
            else:
                print("You are not connected to a voice channel in this server")
                return
        else:
            if ctx.voice_client is None:
                member = ctx.author
                if not member is discord.Member:
                    for guild in bot.guilds:
                        member = guild.get_member(ctx.author.id)
                        if not member:
                            pass
                        elif not member.voice:
                            continue
                if member:
                    if member.voice:
                        target_channel = member.voice.channel
                        await target_channel.connect()
                    else:
                        print("You are not connected to a voice channel.")
                        print("or something is broken. "
                              "maybe try specifying a channel ID if you insist on using the bot though DMs")
                        return
                else:
                    print("Using this bot through DMs without specifying a channel ID, "
                          "requires you enable SERVER MEMBERS INTENT over at "
                          f" https://discord.com/developers/applications/{bot.user.id}/bot")
                    print("then you need to edit this script, uncomment line 22 and comment 23.")
                    print("if you are seeing this message, you haven't did that")
                    return
            elif ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            else:
                return

    if not target_channel:
        print("I am not able to find a channel to join in")
        return

    for voice_client in bot.voice_clients:
        if voice_client.channel == target_channel:
            # ffmpeg -f pulse -i default
            audio_source = discord.FFmpegPCMAudio("default", before_options="-f pulse", options="")
            voice_client.play(audio_source)
            try:
                await ctx.message.add_reaction("✅")
            except:
                print(f"joined {target_channel.name}")


bot.run(bot_token)
