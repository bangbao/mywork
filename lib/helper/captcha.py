# -*- coding: utf-8 -*-

import platform
import random
import string
import cStringIO
from PIL import Image,ImageDraw,ImageFont


def get_font_path():
    """获取字体路径
    """
    name = platform.system()
    # mac
    if name == 'Darwin':
        path = '/Library/Fonts/Songti.ttc'
    # linux
    elif name == 'Linux':
        path = '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf'
    # window
    else:
        path = r'C:\Windows\Fonts\Songti.ttf'
    return path


class RandomChar(object):

    @staticmethod
    def Unicode():
        val = random.randint(0x4E00, 0x9FBF)
        return unichr(val)

    @staticmethod
    def GB2312():
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        tail = random.randint(0, 0xF)
        val = ( head << 8 ) | (body << 4) | tail
        strhex = "%x" % val
        return strhex.decode('hex').decode('gb2312')

    @staticmethod
    def String():
        val = random.choice(string.letters)
        return unichr(val)

    @staticmethod
    def Number():
        val = random.choice(string.digits)
        return unichr(val)

    @staticmethod
    def Strnum():
        pool = random.choice([string.letters, string.digits])
        val = random.choice(pool)
        return unichr(val)


class ImageChar(object):
    def __init__(self, fontColor = (0, 0, 0),
                size = (108, 40),
                fontPath = get_font_path(),
                bgColor = (255, 255, 255),
                fontSize = 20):
        self.size = size
        self.fontPath = fontPath
        self.bgColor = bgColor
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = ImageFont.truetype(self.fontPath, self.fontSize)
        self.image = Image.new('RGB', size, bgColor)
        self.result = []

    def rotate(self):
        self.image.rotate(random.randint(0, 30), expand=0)

    def drawText(self, pos, txt, fill):
        draw = ImageDraw.Draw(self.image)
        draw.text(pos, txt, font=self.font, fill=fill)

    def randRGB(self):
        return (random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))

    def randPoint(self):
        (width, height) = self.size
        return (random.randint(0, width), random.randint(0, height))

    def randLine(self, num):
        draw = ImageDraw.Draw(self.image)
        for i in range(0, num):
            draw.line([self.randPoint(), self.randPoint()], self.randRGB())

    def randChinese(self, num):
        gap = 5
        start = 0
        for i in range(0, num):
            char = RandomChar.GB2312()
            x = start + self.fontSize * i + random.randint(0, gap) + gap * i
            self.drawText((x, random.randint(-5, 5)), char, self.randRGB())
            self.rotate()
            self.randLine(4)
            self.result.append(char)

    def save(self, path):
        self.image.save(path)


def create_captcha(num=4, ext='jpeg'):
    """Captcha
    """
    size = (108, 40)
    color = (255, 255, 255)
    image = Image.new('RGB', size, color=color) # model, size, background color
    # font_file = os.path.join(BASE_DIR, 'static/fonts/ARIAL.TTF') # choose a font file
    font_file = get_font_path()
    font = ImageFont.truetype(font_file, 32) # the font object
    draw = ImageDraw.Draw(image)
    rand_str = ''.join(random.sample(string.letters + string.digits, 4)) # The random string
    draw.text((7, 0), rand_str, fill=(1, 40, 5), font=font) # position, content, color, font
    obj = ImageChar(size=size, fontPath=font_file, bgColor=color)
    for _ in range(4):
        draw.line([obj.randPoint(), obj.randPoint()], obj.randRGB())
    buf = cStringIO.StringIO() # a memory buffer used to store the generated image
    image.save(buf, 'jpeg')
    return rand_str.lower(), buf.getvalue()


if __name__ == '__main__':
    print create_captcha(4)
    #ic = ImageChar(fontColor=(100, 211, 90))
    #ic.randChinese(4)
    #ic.save("1.jpeg")
    #print ','.join(ic.result)