from flask import make_response
from simplexml import dumps
from settings import *
import string
import zipfile
from random import choices
from data.files import Files
import os


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

