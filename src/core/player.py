

from ..source.Basic import TrackList
from .vlc import Vlc


class Mp (Vlc):
    playlist: list[TrackList] = []

    def __init__(self, args=...) -> None:
        super().__init__(args)

    async def player_stopped_callback(self):
        ...

    async def player_end_callback(self):
        return await super().player_end_callback()
