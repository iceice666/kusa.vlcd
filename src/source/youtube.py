from __future__ import unicode_literals

import requests
import youtube_dl

from src import config
from src.source import Basic
from src.source.Basic import Method, Source, Status
from src.source.Basic import Track as _track


class Track(_track):
    source_uri: str
    uri: str
    author: str
    title: str
    last_refresh: float
    refresh_require_time: int = 30 * 60  # secs
    source_status: "Status" = Basic.VIDEO_UNKNOWN


class Youtube(Source):
    @staticmethod
    async def get_source_uri(method: "Method", video: str) -> list[Track]:
        if method is Basic.BY_VIDEO_ID:
            video = f"https://youtu.be/{video}"

        with youtube_dl.YoutubeDL(
            {
                "quiet": True,
                "no_warnings": True,
                "ignoreerrors": True,
            }
        ) as ydl:
            source_info = ydl.extract_info(video, download=False)

        result = Track()
        result.uri = video
        if source_info is None:
            result.source_status = Basic.VIDEO_UNAVABILABLE
            return [result]
        elif source_info.get("_type", None) == "playlist":
            playlist = source_info["entries"]
        else:
            playlist = [source_info]

        if playlist is None:
            result.source_status = Basic.VIDEO_NOT_FOUND
            return [result]

        result = []
        for i in playlist:
            try:
                stream_url = i["formats"][0]["url"]
            except KeyError:
                stream_url = i["formats"][0]["fragment_base_url"]

            track = Track()
            track.uri = i["webpage_url"]
            track.source_uri = stream_url
            track.title = i["title"]
            track.author = i["uploader"]
            track.source_status = Basic.VIDEO_AVABILABLE
            result.append(track)

        return result

    @staticmethod
    async def search(keyword: str) -> list[Track]:
        results = requests.get(
            "https://www.googleapis.com/youtube/v3/search?",
            params={
                "part": "snippet",
                "type": "video",
                "maxResults": "20",
                "search_query": keyword,
                "key": Config.Youtube.API_KEY,
            },
        ).json()

        result = []
        for i in results:
            track = Track()
            track.title = i["snippet"]["title"]
            track.uri = f'https://youtu.be/{i["id"]["videoId"]}'

            result.append(track)

        return result
