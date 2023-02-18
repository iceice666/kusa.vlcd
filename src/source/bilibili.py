import os
import re

import config
from source import Basic
from source.Basic import Method, Source, Status
from source.Basic import Track as _track


class Track(_track):
    uri: str
    title: str
    source_uri: str
    source_status: "Status" = Basic.VIDEO_UNKNOWN


class BiliBili(Source):
    @staticmethod
    async def search(keyword: str) -> list[Track]:
        return []

    @staticmethod
    async def get_source_uri(method: "Method", video: str) -> list[Track]:
        return []
