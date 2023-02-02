import asyncio

import vlc

from ..source.Basic import Track
import abc


class Vlc:
    player: vlc.MediaPlayer
    current_track: Track
    is_skipped: bool = False

    def __init__(self,
                 args=["--no-ts-trust-pcr",
                       "--ts-seek-percent", "--no-video", "-q"]
                 ) -> None:

        self._running_loop = asyncio.get_running_loop()

        self.player = vlc.MediaPlayer([vlc.Instance(args)])
        self.event = vlc.EventType
        self.event_attach = self.player.event_manager().event_attach

        self.player.audio_set_volume(20)

        self.event_attach(
            # i dont know why if i use `vlc.EventType.MediaPlayerEndReach`,
            # pyright says it wrong.
            self.event(265),  # MediaPlayerEndReach

            lambda *_: asyncio.run_coroutine_threadsafe(self.player_end_callback(),
                                                        self._running_loop)
        )

        self.event_attach(
            self.event(262),  # MediaPlaerStopped
            lambda *_: asyncio.run_coroutine_threadsafe(self.player_stopped_callback(),
                                                        self._running_loop)
        )

    @property
    def instance(self):
        return self.player.get_instance()

    @abc.abstractmethod
    async def player_end_callback(self):
        ...

    @abc.abstractmethod
    async def player_stopped_callback(self):
        ...
        self.is_skipped = False

    def load_media(self, media: Track):
        self.current_track = media
        self.player.set_mrl(media.source_uri)

    def play(self):
        self.player.play()

    def skip(self):
        self.is_skipped = True
        self.player.stop()

    def stop(self):
        self.is_skipped = False
        self.player.stop()

    def pause(self):
        self.player.set_pause(1)

    def resume(self):
        self.player.set_pause(0)

    @property
    def position(self):
        return self.player.get_time()

    @property
    def length(self):
        return self.player.get_length()

    @property
    def percent(self):
        return self.player.get_position()

    @property
    def is_playing(self):
        return self.player.is_playing()
