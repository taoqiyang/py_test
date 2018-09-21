from PIL import Image, ImageDraw, ImageFont


def test():
    im = Image.open('test.jpeg')
    # im.show()
    print(im.mode)
    drawer = ImageDraw.Draw(im)

    f = ImageFont.truetype('OpenSans-Bold.ttf', size=20)
    w, h = f.getsize("hello world")
    drawer.text((im.width - w - 5, 5), "hello world", font=f, fill=(0, 0, 255))
    im.show()


if __name__ == '__main__':
    test()
