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
    source_status: "Status"


class Local(Source):
    @staticmethod
    async def search(keyword: str) -> list[Track]:
        r = []
        for root, _, files in os.walk(config.Local.PATH):
            for name in files:
                if re.search(keyword, name) is not None:
                    t = Track()
                    t.uri = os.path.join(root, name)
                    t.source_uri = t.uri
                    t.title = name

        return r

    @staticmethod
    async def get_source_uri(method: "Method", video: str) -> list[Track]:
        if method is Basic.BY_VIDEO_ID:
            path = config.Local.PATH + video
        elif method is Basic.BY_VIDEO_URI:
            path = video
        else:
            return []

        t = Track()
        t.uri = path
        t.source_uri = t.uri
        t.title = os.path.basename(path)
        return [t]
