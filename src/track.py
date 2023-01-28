
class Track:
    def __init__(self, url, source_url):
        self.url = url
        self.source_url = source_url

    def refresh_source(self):
        self.source_url = None
