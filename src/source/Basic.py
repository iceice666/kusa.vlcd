import abc
from typing import NewType


Method = NewType('Method', str)
BY_VIDEO_ID = Method("id")
BY_VIDEO_URL = Method("url")

Status = NewType('Status', str)
VIDEO_AVABILABLE = Status("avabilable")
VIDEO_UNAVABILABLE = Status("unavabilable")
VIDEO_NOT_FOUND = Status("not_found")
VIDEO_UNKNOWN = Status("unknown")


class Source(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    async def get_stream_url() -> 'TrackList':
        '''
        Get playable url(s)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    async def search(keyword):
        pass


class Track(metaclass=abc.ABCMeta):
    url: str
    stream_url: str


class TrackList(list, metaclass=abc.ABCMeta):
    url: str
    last_refresh: float
    refresh_require_time: int  # -1 means wont check
    url_status: 'Status'

    def __init__(self) -> None:
        super().__init__()

    @property
    @abc.abstractmethod
    def is_need_refresh(self) -> bool:
        pass
