from datetime import datetime
from pathlib import Path
from pprint import pprint
from typing import Optional, Union
import urllib3
import aiohttp
import aiofiles

import root.models as models
import root.enums as enums
import root.exceptions as exceptions


async def file_download(url: str, dir_to_save: str):
    file_path = Path(
        dir_to_save,
        str(datetime.utcnow().timestamp()) + '_' + str(Path(url).name)
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(file_path, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return str(file_path), resp.status
