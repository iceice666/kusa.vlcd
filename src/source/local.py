import os.path
import subprocess
import asyncio

from src import Config

from src.source.Basic import Source, Status, Method
from src.source.Basic import Track as _track, TrackList as _tracklist
from src.source import Basic


class Track(_track):
    uri: str
    title: str

    def __init__(self, path="",  title=""):
        self.uri = path
        self.title = title


class TrackList(_tracklist):
    uri: str

    video_status: 'Status' = Basic.VIDEO_UNKNOWN

    def __init__(self,) -> None:
        super().__init__()

    @property
    def is_need_refresh(self) -> bool:
        return False


class Local(Source):
    @staticmethod
    async def search(keyword: str) -> TrackList:
        r = subprocess.run(['fzf', '-f', keyword])

        rl = TrackList()
        if isinstance(r, subprocess.CompletedProcess) and r.stdout is not None:
            sl = str(r.stdout).split('\n')

            [rl.append(Track(Config.Local.PATH+i)) for i in sl]

        return rl

    @staticmethod
    async def get_source_uri(method: 'Method', video: str) -> TrackList:
        r = TrackList()
        if method is Basic.BY_VIDEO_ID:
            path = Config.Local.PATH+video
        elif method is Basic.BY_VIDEO_URI:
            path = video
        else:
            return r

        r.append(Track(path, os.path.basename(path)))
        return r


asyncio.run(Local.search("#1f1e33"))
