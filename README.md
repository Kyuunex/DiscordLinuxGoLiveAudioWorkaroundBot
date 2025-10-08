# Discord Linux Go-Live Audio Workaround Bot

So, this is a Discord bot that will allow you to stream application audio through it 
to a voice channel the exact same way those music bots do.

For the longest time (5+ years) Discord didn't bother to capture Go-Live audio from Linux, during which I made this project. 
Now it does though, but unfortunately, it is mono, and it seems like it is downmixing it server side. 
Good news is, bots don't suffer from this issue, so this project is sticking around for probably 5 more years. 😞

The advantages of using this rather than using audio routing solutions through microphone input of Discord are that:
1. Discord mic input is encoded in mono, while bots can stream stereo audio. Mono audio sounds terrible, 
   especially if you are streaming a rhythm game like osu!
2. You will need to give up noise suppression etc when doing it through the mic.
3. Allow the end user audio level adjustment of the stream audio and your voice individually.
4. End users who don't want to listen to your stream can just mute the bot.

---

## Installation Instructions

1. Pick a .py file from this repo.
    + `go-live-bot-classic.py` -- uses old style prefixed commands, scraping messages.
    + `go-live-bot-slash.py` -- uses slash commands.
2. Make sure the file is executable (`chmod +x go-live-bot-classic.py`)
3. Install discord.py 2.x with some dependencies: 
   + Arch Linux users can do `paru -S python-discord python-pynacl`
   + if you want to create a virtual environment, inside you do `pip3 install discord.py[voice] PyNaCl`
4. Make sure you have `ffmpeg` and `pavucontrol` installed as well.
5. Set `GOLIVE_BOT_TOKEN` environment variable with the bot token or put it in `~/.local/share/go-live-bot/token.txt`

To get a bot token, register a new app [here](https://discord.com/developers/applications), 
create a bot, and copy the token (not the client secret).  
You also need to enable `MESSAGE CONTENT` intent for the classic command version.

## How to use
1. Using the commands bellow, make a virtual audio sink named `STREAM_AUDIO`
    ```sh
    pacmd load-module module-null-sink sink_name=STREAM_AUDIO
    pacmd update-sink-proplist STREAM_AUDIO device.description=STREAM_AUDIO
    ```
    + Note: use `pactl` instead of `pacmd` if you are using PipeWire.
2. Start the bot. (To start the bot, literally run it.)
3. Send application audio to this sink. If you can't do it through the application, try using `pavucontrol` for that.
4. Using the following command, create a stereo virtual audio loopback session.
    ```sh
    pactl load-module module-loopback latency_msec=1 channels=2
    ```
5. Using `pavucontrol` make the loopback device take audio from the monitor of our sink we just made. 
    + For some reason, in `pavucontrol` the sink may show up as `Output to Null Device`. 
    + This is, so you can hear the application audio yourself without a delay.
6. Type `gl.join` or `/join` inside the voice channel you want the bot to join.
    + This will make the bot join and start streaming your microphone.
7. Using `pavucontrol`, locate the recording session that the bot is doing, and change the input the monitor of your STREAM_AUDIO. 
    + For some reason, in `pavucontrol` the sink may show up as `Output to Null Device`
8. profit???
9. When you are done, type `gl.leave` or `/leave` in a chat where the bot can read.
10. After that, you can just right-click in `pavucontrol` on the loopback device and click on terminate. 
    + Or you could just type `pulseaudio -k` in the terminal.  

---

### Help wanted:
The world has moved onto pipewire, so someone please update the instructions to pipewire native commands if there are any.

---

We're coming up on it taking discord a decade to give us properly working Go-Live audio capture on Linux lmao 