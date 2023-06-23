import requests

import uuid

from Helpers.HeicToPng import heic_to_png


def extract_file_extension_from_url(url):
    url = url.lower()
    if '.heic' in url:
        return 'heic'
    elif '.jepg' in url:
        return 'jpeg'
    elif '.jpg' in url:
        return 'jpg'
    else:
        return 'png'


# Print the UUID
def download_image(url, filename):
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    cnt = 0
    while r.content == 0 and cnt < 5:
        open(filename, 'wb').write(r.content)
        cnt += 1
    if extract_file_extension_from_url(url) == "heic":
        return heic_to_png(filename)
    return filename

class ImageCache:
    cache = {}

    @staticmethod
    def get_image(image_url):
        if ImageCache.cache.get(image_url) is None:
            filename = str(uuid.uuid4()) + '.' + extract_file_extension_from_url(image_url)
            filename = download_image(image_url, filename)
            ImageCache.cache[image_url] = filename
        return ImageCache.cache[image_url]
