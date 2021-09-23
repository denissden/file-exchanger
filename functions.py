from settings import *
import string
from datetime import datetime, timedelta
from random import choices
from data.files import Files
from data import db_session
import os
import shutil
import logging
from threading import Timer

P = os.path.abspath

def readable_size(size):
    v = ["B", "KB", "MB", "GB"]
    i = 0
    while size >= 1024:
        size /= 1024
        i += 1
    return '%.2f%s' % (round(size), v[i])


def secure_filename(name):
    for c in NOT_ALLOWED_CHARACTERS:
        name = name.replace(c, "_")
    return name


def custom_link(length):
    characters = string.digits + string.ascii_letters
    download_url = ''.join(choices(characters, k=length))

    try:
        Files.link = download_url
    except Exception:
        return custom_link()

    return download_url


def get_expiration_time(index="0"):
    now = datetime.now()
    try:
        delta = timedelta(**EXPIRATION_IDS[index])
        return now + delta
    except Exception:
        return


def cleanup():
    now = datetime.now()

    removed_count = 0
    s = db_session.create_session()
    expired = s.execute(f'SELECT link FROM files WHERE (expiration_date < "{now}")')
    for element in expired:
        path = P(os.path.join(UPLOAD_FOLDER, element[0]))
        zip_path = P(os.path.join(ZIPS_FOLDER, element[0]) + ".zip")
        if os.path.exists(path):
            shutil.rmtree(path)
            removed_count += 1
        if os.path.exists(zip_path):
            os.remove(zip_path)

    s.execute(f'DELETE FROM files WHERE (expiration_date < "{str(now)}")')
    # if expiration date is for some reason null
    s.execute(f'UPDATE files SET expiration_date = "{get_expiration_time()}" WHERE expiration_date is NULL')
    s.commit()

    logging.debug(f"cleaned {removed_count} files at {now}")


def inc_downloads(link):
    s = db_session.create_session()
    s.execute(f'UPDATE files SET downloads = downloads + 1 WHERE (link == "{link}")')
    s.commit()


def get_dates(link):
    s = db_session.create_session()
    dates = s.execute(f'SELECT created_date, expiration_date FROM files WHERE (link == "{link}")').fetchone()
    u = dates[0][:16]
    e = dates[1][:16]
    return {"upload_date": u,
            "expiration_date": e}

