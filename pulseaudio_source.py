import discord
import subprocess

class PulseAudioSource(discord.AudioSource):
    def __init__(self, device="default"):
        # FFmpeg command to capture from PulseAudio
        self.process = subprocess.Popen(
            [
                "ffmpeg",
                "-f", "pulse",            # use PulseAudio interface
                "-i", device,             # input device name
                "-f", "s16le",            # output format: 16-bit PCM
                "-ar", "48000",           # sample rate required by Discord
                "-ac", "2",               # stereo
                "pipe:1"                  # output to stdout
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=4096
        )

    def read(self):
        # Read 20 ms of audio (48000 Hz * 2 channels * 2 bytes = 192000 bytes/s)
        # 20ms = 3840 bytes
        return self.process.stdout.read(3840)

    def is_opus(self):
        # We are streaming raw PCM, not Opus
        return False

    def cleanup(self):
        self.process.kill()
