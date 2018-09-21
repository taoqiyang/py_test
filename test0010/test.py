from PIL import Image, ImageDraw, ImageFont
import random


def randomPointColor():
    return random.randint(128, 255), random.randint(128, 255), random.randint(128, 255), 255



def randomChar(char_array=list()):
    if char_array is None or len(char_array) == 0:
        for i in range(10):
            char_array.append(str(i))
        for i in range(ord('a'), ord('z') + 1):
            char_array.append(chr(i))
        for i in range(ord('A'), ord('Z') + 1):
            char_array.append(chr(i))
        random.shuffle(char_array)
    return random.choice(char_array)


def randomCharColor():
    return random.randint(0, 128), random.randint(0, 128), random.randint(0, 128), 255


def test():
    count = 4
    width, height = count * 60, 70
    im = Image.new("RGBA", (width, height), color=(255,) * 4)
    draw = ImageDraw.Draw(im)

    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=randomPointColor())

    font = ImageFont.truetype(font='../test0000/OpenSans-Bold.ttf', size=40)
    for i in range(count):
        # angle = random.randint(-15, 15)
        # im_text = Image.new("RGBA", (60, 70))
        # draw_text = ImageDraw.Draw(im_text)
        # draw_text.text((20, 10), randomChar(), font=font, fill=randomCharColor())
        # im.paste(im_text.rotate(angle), (i * 60, 0))

        draw.text((i * 60 + 20, 10), randomChar(), font=font, fill=randomCharColor())

    open()
    im.show()


if __name__ == '__main__':
    test()
