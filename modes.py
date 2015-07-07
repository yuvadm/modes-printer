import cups

from PIL import Image, ImageColor, ImageDraw, ImageFont
from datetime import datetime

BASE_IMAGE = 'base.jpg'
BASE_FONT = 'cutive.ttf'
MATRIX_PADDING = 3
MATRIX_SIZE = 9
MATRIX_PIXEL_SIZE = 80
MATRIX_OFFSET = ((1181 - (MATRIX_PIXEL_SIZE * MATRIX_SIZE)) / 2, 300)
PRINTER = 'Canon_iP7200_series'


class ModesPrinter(object):

    def __init__(self, imstr):
        username, d, dominants, matrix = imstr.split('|')
        self.username = username
        self.date = datetime.strptime(d, '%m%Y').date()
        self.dominants = [ImageColor.getrgb(x) for x in ('#' + dominants[:6], '#' + dominants[6:])]
        self.matrix = bin(int(matrix, 16))[2+MATRIX_PADDING:]
        self.filename = '{}_{}.jpg'.format(self.username, self.date.strftime('%Y_%m'))

    def _debug(self):
        print(self.username, self.date.month, self.date.year, self.dominants, self.matrix)

    def _draw_image_matrix(self):
        for y in range(MATRIX_SIZE):
            for x in range(MATRIX_SIZE):
                start = (
                    MATRIX_OFFSET[0] + (x * MATRIX_PIXEL_SIZE), 
                    MATRIX_OFFSET[1] + (y * MATRIX_PIXEL_SIZE)
                )
                end = (
                    start[0] + MATRIX_PIXEL_SIZE, 
                    start[1] + MATRIX_PIXEL_SIZE
                )
                fill = self.dominants[int(self.matrix[(y * MATRIX_SIZE) + x])]
                self.draw.rectangle([start, end], fill=fill)

    def _draw_image_text(self):
        self.draw.text((300,1100), '@{} / {}'.format(self.username, self.date.strftime('%B %Y')), 
            font=ImageFont.truetype('cutive.ttf', 32), fill=(0,0,0))

    def draw_image(self):
        self.im = Image.open(BASE_IMAGE).convert('RGB')
        self.draw = ImageDraw.Draw(self.im)
        self._draw_image_matrix()
        self._draw_image_text()

    def save_image(self):
        self.im.save(self.filename)

    def print_image():
        conn = cups.Connection()
        conn.printFile(PRINTER, self.filename, 'title', {})

if __name__ == '__main__':
    imstr = 'yuv.adm|062015|9A8D6D736489|eff51f2af82c06071120a'
    mp = ModesPrinter(imstr)
    mp.draw_image()
    mp.save_image()
    mp.print_image()
