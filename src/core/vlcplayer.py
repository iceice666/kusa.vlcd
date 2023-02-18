import asyncio

import vlc

from source.Basic import Track


class MusicPlayer:
    player: vlc.MediaPlayer
    is_skipped: bool = False
    playlist: list[Track] = []
    current_track: Track | None = None

    flag_repeat: bool = False
    flag_loop: bool = False

    def __init__(self, args=["--ts-seek-percent", "--no-video", "-q"]):
        self.player = vlc.MediaPlayer("", *args)
        self.event = vlc.EventType
        self.event_attach = self.player.event_manager().event_attach

        self.player.audio_set_volume(20)

        self.event_attach(
            # i dont know why if i use `vlc.EventType.MediaPlayerEndReach`,
            # pyright says it wrong.
            self.event(265),  # MediaPlayerEndReach
            lambda *_: self.player_end_callback(),
        )

        self.event_attach(
            self.event(262),  # MediaPlayerStopped
            lambda *_: self.player_stopped_callback(),
        )

    @property
    def instance(self):
        return self.player.get_instance()

    def play(self):
        if self.current_track is None and self.playlist:
            media = self.playlist.pop(0)
            self.current_track = media
            self.player.set_mrl(media.source_uri)
        self.player.play()

    def player_stopped_callback(self):
        if self.is_skipped:
            self.is_skipped = False
            if self.flag_loop and self.current_track is not None:
                self.playlist.append(self.current_track)

            media = self.playlist.pop(0)
            self.current_track = media
            self.player.set_mrl(media.source_uri)
            self.player.play()

    def player_end_callback(self):
        if self.current_track is not None:
            if self.flag_repeat:
                media = self.current_track

            else:
                media = self.playlist.pop(0)

            if self.flag_loop:
                self.playlist.append(self.current_track)

            self.current_track = media
            self.player.set_mrl(media.source_uri)
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

    def toggle_repeat(self):
        self.flag_repeat = not self.flag_repeat

    def toggle_loop(self):
        self.flag_loop = not self.flag_loop

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
