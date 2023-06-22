import requests

import uuid
# Print the UUID
def download_image(url,filename):
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    cnt = 0
    while (r.content == 0 and cnt < 5):
        open(filename, 'wb').write(r.content)
        cnt += 1
class ImageCache():
    cache = {}
    def getImage(imageUrl):
        if(ImageCache.cache.get(imageUrl) is None):
            filename = str(uuid.uuid4())+'.png'
            download_image(imageUrl,filename)
            ImageCache.cache[imageUrl] = filename
        return ImageCache.cache[imageUrl]