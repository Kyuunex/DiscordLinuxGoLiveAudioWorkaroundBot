# Discord Linux Go-Live Audio Workaround Bot 

## Good news!
This project is mostly obsolete. As of Early 2025, Go Live does capture audio on Discord now, 
it does capture only one channel with my testing but it's better than nothing. 

## What this does
So, this is a Discord bot that will allow you to stream application audio through it 
to a voice channel the exact same way those music bots do.

The advantages of using this rather than using audio routing solutions through microphone input of Discord are that:
1. Discord mic input is encoded in mono, while bots can stream stereo audio. Mono audio sounds terrible, 
   especially if you are streaming a rhythm game like osu!
2. You will need to give up noise suppression etc when doing it through the mic.
3. Allow the end user audio level adjustment of the stream audio and your voice individually.
4. End users who don't want to listen to your stream can just mute the bot.

---

## Installation Instructions

1. Pick a .py file from this repo, name it what you want and put it in your PATH if you want to.
    + `go-live-bot-classic.py` -- uses old style prefixed commands, scraping messages.
    + `go-live-bot-slash.py` -- uses slash commands. **(This one is still work in progress. Use classic.)**
2. Make the file executable `chmod +x go-live-bot-classic.py`
3. Install discord.py 2.x with voice support: `pip3 install discord.py==2.2.2`
    + You may also need to install `PyNaCl` using: `pip3 install PyNaCl`
4. Make sure you have `ffmpeg` and `pavucontrol` installed.
5. Set `GOLIVE_BOT_TOKEN` environment variable with the bot token. 

To get a bot token, register a new app [here](https://discord.com/developers/applications), 
create a bot, and copy the token (not the client secret).  
You also need to enable `MESSAGE CONTENT` intent for the classic command version 
and `SERVER MEMBERS` intent for being able to use the join commands in DMs without specifying a channel ID.

## How to use
1. Using the commands bellow, make a virtual audio sink named `STREAM_AUDIO`
    ```sh
    pacmd load-module module-null-sink sink_name=STREAM_AUDIO
    pacmd update-sink-proplist STREAM_AUDIO device.description=STREAM_AUDIO
    ```
    + Note: use `pactl` instead of `pacmd` if you are using PipeWire.
    + (optional, experimental) At the top of the file in `FFMPEG_PULSEAUDIO_SOURCE`, you can put `CUSTOM_SINK.monitor` and skip step 7. 
2. Start the bot. (To start the bot, literally run it.)
3. Send application audio to this sink. If you can't do it through the application, try using `pavucontrol` for that.
4. Using the following command, create a stereo virtual audio loopback session.
    ```sh
    pactl load-module module-loopback latency_msec=1 channels=2
    ```
5. Using `pavucontrol` make the loopback device take audio from the monitor of our sink we just made. 
    + For some reason, in `pavucontrol` the sink may show up as `Output to Null Device`. 
    + This is, so you can hear the application audio yourself without a delay.
6. Type `/join` (optionally followed by the voice channel ID in a chat where the bot can read). 
    + This will make the bot join and start streaming your microphone.
7. Using `pavucontrol`, locate the recording session that the bot is doing, and change the input the monitor of your STREAM_AUDIO. 
    + For some reason, in `pavucontrol` the sink may show up as `Output to Null Device`
8. profit???
9. When you are done, type `/leave` in a chat where the bot can read.
10. After that, you can just right-click in `pavucontrol` on the loopback device and click on terminate. 
    + Or you could just type `pulseaudio -k` in the terminal.  

---

### Known issue + Help wanted:
If you get an error like `default: Generic error in an external library`, I have no idea what causes this.  
You are welcome to find a solution and make a PR or create an issue. I'll investigate when I have time.

---

Note: if you are having problems with audio cutting out, 
try `export PULSE_LATENCY_MSEC=5`

