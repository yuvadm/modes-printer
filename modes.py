import cups

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

BASE_IMAGE = 'base.jpg'
BASE_FONT = 'cutive.ttf'
PRINTER = 'Canon_iP7200_series'


class ModesPrinter(object):

    def __init__(self, imstr):
        username, d, dominants, matrix = imstr.split('|')
        self.username = username
        self.date = datetime.strptime(d, '%m%Y').date()
        self.dominants = [dominants[:6], dominants[6:]]
        self.matrix = bin(int(matrix, 16))[5:]

    def _debug(self):
        print(self.username, self.date.month, self.date.year, self.dominants, self.matrix)

    def draw_image(self):
        im = Image.open(BASE_IMAGE)
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype('cutive.ttf', 32)
        draw.text((10, 25), '@{} / {}'.format(self.username, self.date.strftime('%B %Y')), font=font)
        im.show()

    def print_image():
        conn = cups.Connection()
        conn.printFile(PRINTER, 'base.jpg', 'title', {})

if __name__ == '__main__':
    imstr = 'yuv.adm|062015|9A8D6D736489|eff51f2af82c06071120a'
    mp = ModesPrinter(imstr)
    mp.draw_image()
