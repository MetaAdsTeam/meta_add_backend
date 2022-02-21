import logging
import os
import string
from datetime import datetime, date
from pathlib import Path
from typing import Union, Optional

import aiofiles
import aiohttp
import cv2
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


def safe_filename(filename: str) -> str:
    allowed_chars = string.digits + string.ascii_letters + '.'
    return ''.join(filter(lambda c: c in allowed_chars, filename))


def is_image(filename: str) -> bool:
    return filename.rsplit('.', 1)[-1] in [
        'jpg', 'jpeg', 'jfif', 'pjpeg', 'pjp', 'apng', 'png',
        'svg', 'webp', 'gif', 'bmp', 'ico', 'tif', 'tiff'
    ]


def make_thumbnail(filepath: str, target_side_size: int = 350) -> Optional[str]:
    filename = os.path.basename(filepath).rsplit('.', 1)[0]
    dirname = os.path.dirname(filepath)
    save_on_filename = os.path.join(dirname, f'thumb_{filename}.png')
    max_side_size = target_side_size * 2
    try:
        if is_image(filepath):
            im_ar = cv2.imread(filepath)
        else:
            v_cap = cv2.VideoCapture(filepath)
            res, im_ar = v_cap.read()
            frames = 1000
            while res and (im_ar.mean() < 25 or im_ar.mean() > 240) and frames:
                res, im_ar = v_cap.read()
                frames -= 1
            if im_ar is None:
                _, im_ar = cv2.VideoCapture(filepath).read()

        height, width, _ = im_ar.shape
        sides_swapped = False
        if height > width:
            width, height = height, width
            sides_swapped = True

        target_height = min(target_side_size, max(height, target_side_size))
        target_width = round(width / (height / target_height))

        if target_width > max_side_size:
            # The case where one side / other side > 2
            target_height = round(target_height / (target_width / max_side_size))
            target_width = max_side_size

        if sides_swapped:
            target_width, target_height = target_height, target_width

        im_ar = cv2.resize(im_ar, (target_width, target_height), 0, 0, cv2.INTER_LINEAR)
        cv2.imwrite(save_on_filename, im_ar)
        return save_on_filename
    except Exception as e:
        logging.getLogger('utils').exception(e, exc_info=True)
        return None
