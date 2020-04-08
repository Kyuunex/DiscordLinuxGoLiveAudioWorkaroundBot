import discord

from discord.ext import commands
from modules import permissions


class AudioStream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stop")
    @commands.check(permissions.is_admin)
    @commands.guild_only()
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send(f":ok_hand:")

    @commands.command(name="start")
    @commands.check(permissions.is_admin)
    @commands.guild_only()
    async def start(self, ctx):
        async with ctx.typing():
            # ffmpeg -f pulse -i default
            audio_source = discord.FFmpegPCMAudio("default", before_options="-f pulse", options="")
            ctx.voice_client.play(audio_source)
        await ctx.send(f":ok_hand:")

    @start.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(AudioStream(bot))
