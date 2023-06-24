import requests

import uuid


# Print the UUID
def download_image(url, filename):
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    cnt = 0
    while (r.content == 0 and cnt < 5):
        open(filename, 'wb').write(r.content)
        cnt += 1


class ImageCache:
    cache = {}

    @staticmethod
    def get_image(image_url):
        if ImageCache.cache.get(image_url) is None:
            filename = str(uuid.uuid4()) + '.png'
            download_image(image_url, filename)
            ImageCache.cache[image_url] = filename
        return ImageCache.cache[image_url]
