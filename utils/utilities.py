import os

from settings import RESOURCES


def template(name: str):
    return os.path.join(RESOURCES, 'layouts', name)


def static(name: str):
    return os.path.join(RESOURCES, 'images', name)
