#!/usr/bin/env python3
import discord
import sys
import os

# This version is only tested on Py-cord. When discord.py devs decided to shut down the project,
# I moved the project to Py-cord, and got the slash commands somewhat working.
# Since discord.py returned, I am in a process of moving back to it.
# And so, this version of the bot does not work with discord.py.
# It requires a lot of work to get it to work. Contributions are appreciated.
# Meanwhile you can use the classic version of this bot with prefixed commands!


FFMPEG_PULSEAUDIO_SOURCE = "default"  # you can change this to CUSTOM_SINK.monitor (EXPERIMENTAL)
OPUS_ENCODE_BITRATE = 48  # Kbps

if os.environ.get('GOLIVE_BOT_TOKEN'):
    bot_token = os.environ.get('GOLIVE_BOT_TOKEN')
else:
    # bot_token = ""  # You can also put your bot token here, uncomment this line and comment the next line
    sys.exit("please set GOLIVE_BOT_TOKEN env var to your bot token")

owner_list = []

# intents = discord.Intents.default()
# intents.members = True
# bot = commands.Bot(intents=intents)
bot = discord.Bot()


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
    print(f"Available commands:")
    print(f"/join <channel_id>")
    print(f"/leave")
    print(f"------")


@bot.slash_command()
async def leave(ctx):
    if not int(ctx.author.id) in owner_list:
        return
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()
    try:
        await ctx.respond(":ok_hand:")
    except discord.Forbidden:
        print("channel left")


@bot.slash_command()
async def join(ctx, channel_id=None):
    if not int(ctx.author.id) in owner_list:
        return

    target_channel = None

    if channel_id:
        target_channel = bot.get_channel(int(channel_id))
        if not target_channel:
            await ctx.respond("can't find a channel with that ID")
            return
        await target_channel.connect()
    else:
        if ctx.guild:
            if ctx.author.voice:
                target_channel = ctx.author.voice.channel
                await target_channel.connect()
            else:
                await ctx.respond("You are not connected to a voice channel in this server")
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
                    print("then you need to edit this script, uncomment line 16 and comment 17.")
                    print("if you are seeing this message, you haven't did that")
                    return
            elif ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            else:
                return

    if not target_channel:
        await ctx.respond("I am not able to find a channel to join in")
        return

    for voice_client in bot.voice_clients:
        if voice_client.channel == target_channel:
            # ffmpeg -f pulse -i default -map_metadata -1
            # -f opus -c:a libopus -ar 48000 -ac 2 -b:a 48k
            # -loglevel warning -application lowdelay pipe:1

            audio_source = discord.FFmpegOpusAudio(
                FFMPEG_PULSEAUDIO_SOURCE,
                bitrate=OPUS_ENCODE_BITRATE,
                before_options="-f pulse",
                options="-application lowdelay"
            )
            
            voice_client.play(audio_source)
            await ctx.respond(f"joined {target_channel.mention}")


bot.run(bot_token)
