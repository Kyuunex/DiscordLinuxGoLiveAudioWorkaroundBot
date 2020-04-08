# DiscordLinuxGoLiveAudioWorkaroundBot 
It's been months since Go Live was rolled out for Linux users of Discord 
but as of 2020/04/08, they still haven't fixed the audio streaming for it. 
I am tired of waiting, so I wrote a workaround bot. This bot will allow you to stream audio through it. 
The advantage of using this rather than using audio routing solutions through microphone input of discord is that 
discord mic input is encoded in mono, while bots can stream stereo audio.

---

## Installation Instructions

1. Install `git` and `Python 3.6` (or newer) if you don't already have them.
2. Clone this repository using this command `git clone https://github.com/Kyuunex/Momiji.git`
3. Make sure you have `ffmpeg` and `pavucontrol` installed.
4. Create a folder named `data`, then create `token.txt` inside it. Then put your bot token in it. 
5. To start the bot, run `DiscordLinuxGoLiveAudioWorkaroundBot.py`.

## How to use

1. Start the bot. If it's the first time you are starting the bot, restart the bot.
2. Type `golive.start`. This will make the bot join and start streaming your microphone.
3. Using `pavucontrol`, you can feed the appropriate input to the bot. I recommend feeding a Virtual Loopback device.
4. profit???

## Making a virtual loopback device.
```sh
pacmd load-module module-null-sink sink_name=CABLE
pacmd update-sink-proplist CABLE device.description=CABLE
pactl load-module module-loopback latency_msec=1
```
