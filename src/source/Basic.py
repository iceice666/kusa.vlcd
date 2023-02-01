import abc
from typing import NewType


Method = NewType('Method', str)
BY_VIDEO_ID = Method("id")
BY_VIDEO_URI = Method("uri")

Status = NewType('Status', str)
VIDEO_AVABILABLE = Status("avabilable")
VIDEO_UNAVABILABLE = Status("unavabilable")
VIDEO_NOT_FOUND = Status("not_found")
VIDEO_UNKNOWN = Status("unknown")


class Source(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    async def get_source_uri() -> 'TrackList':
        '''
        Get playable url(s)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    async def search(keyword):
        pass


class Track(metaclass=abc.ABCMeta):
    uri: str
    source_uri: str


class TrackList(list, metaclass=abc.ABCMeta):
    uri: str
    last_refresh: float
    refresh_require_time: int  # -1 means wont check
    source_status: 'Status'

    def __init__(self) -> None:
        super().__init__()

    @property
    @abc.abstractmethod
    def is_need_refresh(self) -> bool:
        pass
