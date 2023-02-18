import asyncio

from core import vlcplayer
from source.bilibili import BiliBili
from source.local import Local
from source.youtube import Youtube


class CLI:
    player: vlcplayer.MusicPlayer

    def __init__(self, player: vlcplayer.MusicPlayer):
        self.player = player

        self.search_dispatcer = {
            "youtube": Youtube.search,
            "bilibili": BiliBili.search,
            "local": Local.search,
        }

    def search(self, cmd):
        platform = cmd[1]
        keyword = cmd[2]

        p = self.search_dispatcer.get(
            platform,
        )
        if p is not None:
            result = asyncio.run_coroutine_threadsafe(
                p(keyword), asyncio.get_running_loop()
            ).result()

            self.player.playlist.extend(*result)

    async def main(self):
        while True:
            try:
                cmd_args = input("> ").split(" ")
                cmd = cmd_args.pop(0)
                match cmd:
                    case "play" | "p":
                        self.player.play()

                    case "skip" | "s":
                        self.player.skip()

                    case "stop" | "S":
                        self.player.stop()

                    case "pause" | "P":
                        self.player.pause()

                    case "resume" | "r":
                        self.player.resume()

                    case "exec" | ":":
                        exec(" ".join(cmd_args).replace("$", "self.player.player."))
                        ...

                    case "search" | "?":
                        platform = cmd_args[0]
                        keyword = cmd_args[1]
                        r = []

                        match platform:
                            case "local":
                                r = await Local.search(keyword)

                            case "bilibili":
                                r = await BiliBili.search(keyword)

                        self.player.playlist.extend(r)

            except Exception as e:
                print(e)
