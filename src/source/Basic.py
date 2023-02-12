import abc
from typing import NewType

Method = NewType("Method", str)
BY_VIDEO_ID = Method("id")
BY_VIDEO_URI = Method("uri")

Status = NewType("Status", str)
VIDEO_AVABILABLE = Status("avabilable")
VIDEO_UNAVABILABLE = Status("unavabilable")
VIDEO_NOT_FOUND = Status("not_found")
VIDEO_UNKNOWN = Status("unknown")


class Track(metaclass=abc.ABCMeta):
    uri: str
    source_uri: str
    source_status: "Status"


class Source(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    async def get_source_uri() -> list[Track]:
        """
        Get playable url(s)
        """
        pass

    @staticmethod
    @abc.abstractmethod
    async def search(keyword):
        pass
