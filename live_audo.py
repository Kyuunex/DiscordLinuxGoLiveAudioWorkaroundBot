import discord
import sounddevice as sd

class LiveAudioSource(discord.AudioSource):
    def __init__(self, samplerate=48000, channels=2, blocksize=960):
        # 960 frames = 20ms @ 48kHz
        self.stream = sd.InputStream(
            samplerate=samplerate,
            channels=channels,
            dtype='int16',
            blocksize=blocksize,
        )
        self.stream.start()

    def read(self):
        data, _ = self.stream.read(960)  # 20 ms of audio
        return data.tobytes()

    def is_opus(self):
        return False

    def cleanup(self):
        self.stream.stop()
        self.stream.close()
