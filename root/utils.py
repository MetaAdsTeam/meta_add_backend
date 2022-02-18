from datetime import datetime, date
from pathlib import Path
from typing import Union

import aiofiles
import aiohttp
import pytz


def proper_utc_date(iso_string: str) -> datetime:
    dt = datetime.fromisoformat(iso_string.removesuffix('Z'))
    if dt.tzinfo is not None:
        dt = dt.astimezone(pytz.UTC)
        dt = dt.replace(tzinfo=None)
    return dt


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


def cut_timezone(dt: datetime):
    if dt.tzinfo is not None:
        dt = dt.astimezone(pytz.UTC).replace(tzinfo=None)
    return dt


def proper_dt_iso(dt: Union['datetime', 'date']):
    if isinstance(dt, datetime):
        dt = cut_timezone(dt)
    return dt.isoformat()
