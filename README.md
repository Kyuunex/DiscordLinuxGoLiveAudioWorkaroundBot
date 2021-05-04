# Discord Linux Go-Live Audio Workaround Bot 
It's been over a year since Go Live was rolled out for Linux users of Discord, 
but as of 2021/05/04, 
they still haven't fixed the issue where audio is not being captured from the application that is being streamed.
You can call this a missing feature if you really want to be technical, but an 'average' end user will disagree.

In fact, they actually denied my bug report
![](https://i.imgur.com/nBfuX4q.png)  
with the following reason  
![](https://i.imgur.com/qMBF3PP.png)  

I would have been happy if they at least gave us some sort of workaround, like starting a capture from an automatically 
created sink and telling us to divert app audio to it, and it will be sent the same way 
the Go Live audio is sent, but nope.

So, a while ago, I wrote a workaround bot. This bot will allow you to stream audio through it. 
The advantages of using this rather than using audio routing solutions through microphone input of discord are that:
1. discord mic input is encoded in mono, while bots can stream stereo audio. Mono audio sounds terrible, 
   especially if you are streaming a rhythm game like osu!
2. You will need to give up noise suppression etc when doing it through the mic.
3. Allow the end user audio level adjustment of the stream audio and your voice individually.
4. Not everyone wants to listen to your stream, so, they won't be forced to listen to it.

To clarify, this bot will stream the audio to a voice channel the exact same way those music bots do.

---

## Installation Instructions

1. Literally get the .py file from this repo, name it what you want and put it in your PATH if you want to.
2. Make sure you have `ffmpeg` and `pavucontrol` installed.
4. Set `GOLIVE_BOT_TOKEN` env var with the bot token. 
4. Set `GOLIVE_BOT_PREFIX` env var with your desired command prefix. (optional, default is `gl.`)
5. To start the bot, literally run it.

In case you don't know, to get a bot token, register a new app [here](https://discord.com/developers/applications), 
create a bot, and copy the token. not the client secret. the token.

## How to use
1. Start the bot. 
2. Using the commands bellow, make a virtual audio sink named `STREAM_AUDIO`
    ```sh
    pacmd load-module module-null-sink sink_name=STREAM_AUDIO
    pacmd update-sink-proplist STREAM_AUDIO device.description=STREAM_AUDIO
    ```
3. Send application audio to this sink. If you can't do it through the application, try using `pavucontrol` for that.
4. Using the following command, create a stereo virtual audio loopback session. 
   Using `pavucontrol` make the loopback device take audio from the monitor of our sink we just made. 
   For some reason, in `pavucontrol` the sink may show up as `Output to Null Device`. 
   This is, so you can hear the application audio yourself without a delay.
    ```sh
    pactl load-module module-loopback latency_msec=1 channels=2
    ```
5. Type `gl.join` (optionally followed by the voice channel ID in a chat where the bot can read). 
   This will make the bot join and start streaming your microphone.
6. Using `pavucontrol`, locate the recording session that the bot is doing, 
   and change the input the monitor of your STREAM_AUDIO. 
   For some reason, in `pavucontrol` the sink may show up as `Output to Null Device`
7. profit???
8. When you are done, type `gl.leave` in a chat where the bot can read.
9. After that, you can just right-click in `pavucontrol` on the loopback device and click on terminate. 
   Or you could just type `pulseaudio -k` in the terminal.

---

## My adventures of exploring this bug.
I explored this bug greatly, 
apparently it's a [bug in electron from 3 and a half years ago](https://github.com/electron/electron/issues/10515) but 
it was closed without actually being fixed.
I explored many solutions to this problem, spent countless hours on it 
and making this bot was the best solution I could come up at the time.
### Other solutions I tried, include:
1. Streaming through the web version
    - ~~Tried in Chromium~~
        - ~~Even the `Share audio` button does not work when sharing a tab~~
    - ~~Tried in Firefox~~
        - ~~Discord normally won't let you, so I had to set the user agent to represent Chromium~~
            - ~~UPDATE: user agent spoofing is no longer needed~~
    - ~~Even on Windows, streaming using the web version in Chrome does not capture audio~~
        - ~~Even when streaming just a tab and checking `Share audio` button~~
    - ~~Not sure if this is broken in the web app, or the Chrome/Chromium is broken.~~
        - ~~If on the web app, perhaps a browser extension can fix this? I'm not good enough to make one~~
        - ~~UPDATE: this was a bug with discord~~
    - UPDATE, I reported this [bug](https://bugs.discord.com/T956) and after several months, they marked it as fixed, 
      around the time they added this feature to mac. 
        - But it applies noise suppression on it. But at the time I reported it, it transported no audio at all. 
          Maybe this will be fixed in few weeks? if not I will just file a new bug report.
        - But having this only limits us to screen-sharing browser tabs with sound. It's better than nothing I guess.
            - Maybe we could use obs/ffmpeg to stream to a browser tab and screen-share a playback of that? 
              we could also locally mute the tab while it's still sharing audio
            - Or maybe someone can convince the Chromium devs to add this for Linux as well. Maybe through PipeWire?
2. Running Windows version of Discord in wine. 
    - The screen-share would not work. The `DiscordHookHelper.exe` would crash. 
      Tried various options relating to Hardware acceleration on/off, didn't help.
3. Dedicated, real Windows environment for running discord.
    - OBS streaming to a custom RTMP server and screen-sharing a mpv playback of that. 
      Creating a virtual audio output devices and make obs pick up audio from that, so voice loopback wouldn't happen
        - This is painfully slow in a vm
        - This can be done on a dedicated computer through LAN 
          but there is a good 5-second delay which I was not able to reduce
            - Most of the delay is probably happening during the encoding. 
              Maybe we could move to an `ffmpeg` based solution?
    - Capturing with a capture card and doing a USB pass-through to a VM, 
      playing back with mpv or vlc and screen-sharing that. 
        - Still need to deal with playing back audio, vlc can do both video and audio at the same time
        - Capture cards are expensive, cheap ones have mediocre quality both video and audio wise. 
          the $16 MACROSILICON one has mono audio anyways, which defeats the purpose of all this, mostly.
        - Painfully slow in a vm probably
        - Could happen on a dedicated pc, 
          could probably send audio through aux or network somehow if capture card does mono,
          mpv is very flexible
    - But seriously, just playing back a video stream in a vm takes a sizable amount of processing power.
    - Did I mention that attempting to screen-share in VMWare blue-screens the whole VM? Well, 
      unless you disable Hardware Acceleration in Virtual machine settings.
    - For a solution like this, using `ffmpeg` with a custom rtmp server sounds like the best idea. 
      on the windows end, we screen-share a mpv view.
4. Using [discord_arch_electron](https://aur.archlinux.org/packages/discord_arch_electron/) package from AUR. 
   this uses system installation of electron instead of what discord bundles. 
    - So in an event this bug is fixed in electron, we may get the fix instantly (very unlikely, read next section)
    - I'm not good enough to just fix this bug but this is a good starting point if you want to give it a try
        - and maybe give them a PR after fixing, and if they reject it, 
          just make a PKGBUILD repo that applies your patch, put on GitHub, doesn't matter.
        - This is like, the best solution to this problem, if you are good enough. 
5. A BetterDiscord plugin
    - I tried this approach as well and got absolutely nowhere, due to the lack of experience I have.
    - This could go along with [discord_arch_electron](https://aur.archlinux.org/packages/discord_arch_electron/) 
      in an event this is fixed in electron.
    - Maybe if there is someone who knows how to make BetterDiscord plugins could rig something up?
        - Maybe give us a sink we can direct audio to.
    - Since this was fixed on a Mac, maybe someone could try that 'Emulator' plugin BD has 
      when it gets updated on canary and see where it goes
6. Reverse engineer how Discord sends a stream and make a small console based app to run an encode with and stream.
   - preferably it would just emulate an RTMP server where OBS or ffmpeg would stream to, 
     and it would forward that to discord.
      - although, discord does not stream in h264, it streams in vp9 iirc to save bandwidth.
        or maybe it depends.
   - No discord bot lib has implemented something like this, so you're on your own
   - having a client that does not behave 100% like discord servers expect it to, 
     may flag your account and get you banned. 
     but hey, what else do we linux users even expect for companies like these?
     
I'd say 