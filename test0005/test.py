import os
from PIL import Image


def test():
    filenames = next(os.walk('images'))[2]
    size = (777, 777)
    for filename in filenames:
        fp = 'images' + os.sep + filename
        im = Image.open(fp)
        im.thumbnail(size)
        im.save(fp)

if __name__ == '__main__':
    test()
