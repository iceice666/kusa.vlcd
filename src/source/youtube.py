from __future__ import unicode_literals
import youtube_dl
import time
import requests
from src.source.Basic import Source, Method, Status
from src.source.Basic import Track as _track, TrackList as _tracklist
from src.source import Basic
from src import Config


class Track(_track):
    source_uri: str
    uri: str
    author: str
    title: str

    def __init__(self, uri="", source_uri="", title="", author=""):
        self.source_uri = source_uri
        self.uri = uri
        self.title = title
        self.author = author


class TrackList(_tracklist):
    uri: str
    last_refresh: float
    refresh_require_time: int = 30*60  # secs
    source_status: 'Status' = Basic.VIDEO_UNKNOWN

    def __init__(self,) -> None:
        super().__init__()
        self.last_refresh = time.time()

    @property
    def is_need_refresh(self) -> bool:
        return time.time() >= self.last_refresh+self.refresh_require_time

    async def refresh(self):
        if self.is_need_refresh:
            self = Youtube.get_source_uri(Basic.BY_VIDEO_URI, self.uri)


class Youtube(Source):
    @staticmethod
    async def get_source_uri(method: 'Method', video: str) -> 'TrackList':
        if method is Basic.BY_VIDEO_ID:
            video = f'https://youtu.be/{video}'

        with youtube_dl.YoutubeDL(
            {"quiet": True, "no_warnings": True,
                "ignoreerrors": True, }
        ) as ydl:

            source_info = ydl.extract_info(video, download=False)

        result = TrackList()
        result.uri = video
        if source_info is None:
            result.source_status = Basic.VIDEO_UNAVABILABLE
            return result
        elif source_info.get('_type', None) == 'playlist':
            playlist = source_info['entries']
        else:
            playlist = [source_info]

        if playlist is None:
            result.source_status = Basic.VIDEO_NOT_FOUND
            return result

        for i in playlist:
            try:
                stream_url = i["formats"][0]["url"]
            except KeyError:
                stream_url = i["formats"][0]["fragment_base_url"]

            result.append(Track(
                uri=i['webpage_url'],
                source_uri=stream_url,
                title=i['title'],
                author=i['uploader']
            ))
        result.source_status = Basic.VIDEO_AVABILABLE
        return result

    @staticmethod
    async def search(keyword: str) -> 'TrackList':
        results = requests.get("https://www.googleapis.com/youtube/v3/search?",
                               params={
                                   "part": "snippet",
                                   "type": "video",
                                   "maxResults": "20",
                                   "search_query": keyword,
                                   "key": Config.Youtube.API_KEY
                               }).json()

        _r = TrackList()
        for i in results:
            _r.append(Track(
                title=i['snippet']['title'],
                uri=f'https://youtu.be/{i["id"]["videoId"]}'
            ))

        return _r
