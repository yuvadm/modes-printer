import cups

from PIL import Image, ImageDraw, ImageFont

BASE_IMAGE = 'base.jpg'
BASE_FONT = 'cutive.ttf'
PRINTER = 'Canon_iP7200_series'


class ModesPrinter(object):

    def __init__(self, imstr):
        username, date, dominants, matrix = imstr.split('|')
        self.username = username
        self.month = date[:2]
        self.year = date[2:]
        self.dominants = [dominants[:6], dominants[6:]]
        self.matrix = bin(int(matrix, 16))[5:]

    def _debug(self):
        print(self.username, self.month, self.year, self.dominants, self.matrix)

    def draw_image(self):
        im = Image.open('base.jpg')
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype('cutive.ttf', 14)
        draw.text((10, 25), 'world', fonts=font)
        im.show()

    def do_print():
        conn = cups.Connection()
        conn.printFile(PRINTER, 'base.jpg', 'title', {})

if __name__ == '__main__':
    imstr = 'yuv.adm|062015|9A8D6D736489|eff51f2af82c06071120a'
    mp = ModesPrinter(imstr)
    mp._debug()
