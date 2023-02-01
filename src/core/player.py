

from src.source.Basic import TrackList
from src.core.vlc import Vlc


class Mp (Vlc):
    playlist: list[TrackList] = []
    current_tracklist: TrackList

    flag_repeat: bool = False
    flag_loop: bool = False

    def __init__(self, args=...) -> None:
        super().__init__(args)

    async def player_stopped_callback(self):
        if self.is_skipped:
            self.is_skipped = False
            if self.flag_loop:
                self.current_tracklist.append(self.current_track)

            self.play()

    async def player_end_callback(self):
        if self.flag_repeat:
            track = self.current_track

        else:
            track = self.current_tracklist.pop(0)

        if self.flag_loop:
            self.current_tracklist.append(self.current_track)

        self.load_media(track)
        self.play()
