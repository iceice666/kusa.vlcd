import asyncio

from core.vlcplayer import MusicPlayer
from ui.cli import CLI


async def main():
    app = CLI(MusicPlayer())
    await app.main()


asyncio.run(main())
