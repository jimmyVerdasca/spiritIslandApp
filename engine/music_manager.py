from kivy.core.audio import SoundLoader


class MusicManager:

    sound = None

    @classmethod
    def start(cls):

        # Don't start it twice
        if cls.sound is not None:
            return

        cls.sound = SoundLoader.load(
            "assets/home/Spirit Island Theme.mp3"
        )

        if cls.sound is None:
            print("Could not load background music.")
            return

        cls.sound.loop = True
        cls.sound.volume = 0.5
        cls.sound.play()

        print("Background music started.")

    @classmethod
    def stop(cls):

        if cls.sound is not None:
            cls.sound.stop()

    @classmethod
    def set_volume(cls, volume):

        if cls.sound is not None:
            cls.sound.volume = volume
