import cups
import redis
import requests
import sys

from PIL import Image, ImageColor, ImageDraw, ImageFont
from datetime import datetime
from time import sleep

ROOT_URL = 'http://10.55.55.229:3000/prints'
BASE_IMAGE = 'base.jpg'
BASE_FONT = 'cutive.ttf'
MATRIX_PADDING = 3
MATRIX_SIZE = 9
MATRIX_PIXEL_SIZE = 80
MATRIX_OFFSET = ((1181 - (MATRIX_PIXEL_SIZE * MATRIX_SIZE)) / 2, 300)
PRINTER = 'Canon_iP7200_series'

r = redis.StrictRedis(host='localhost', port=6379, db=0)

class ModesPrinter(object):

    def __init__(self, imstr):
        username, d, dominants, matrix = imstr.split('|')
        self.username = username
        self.date = datetime.strptime(d, '%m%Y').date()
        self.dominants = [ImageColor.getrgb(x) for x in ('#' + dominants[:6], '#' + dominants[6:])]
        self.matrix = bin(int(matrix, 16))[2+MATRIX_PADDING:]
        self.filename = 'photos/{}_{}.jpg'.format(self.username, self.date.strftime('%Y_%m'))

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
        font = ImageFont.truetype('cutive.ttf', 48)
        text = '@{} / {}'.format(self.username, self.date.strftime('%B %Y'))
        size = font.getsize(text)
        self.draw.text(((1181 / 2) - (size[0] / 2),1100), text, font=font, fill=(0,0,0))

    def draw_image(self):
        self.im = Image.open(BASE_IMAGE).convert('RGB')
        self.draw = ImageDraw.Draw(self.im)
        self._draw_image_matrix()
        self._draw_image_text()

    def save_image(self):
        self.im.save(self.filename)

    def print_image(self):
        conn = cups.Connection()
        conn.printFile(PRINTER, self.filename, 'title', {})

    def show_image(self):
        self.im.show()

    def process_image(self):
        self.draw_image()
        self.save_image()
        self.print_image()

    def test_image(self):
        self.draw_image()
        self.show_image()


def process_jobs(jobs):
    for job in jobs:
        jobkey = 'jobs:{}'.format(job['data'])
        if r.get(jobkey):
            continue
        else:
            print('{} :: Got job {}'.format(datetime.now().isoformat(), job['data']))
            ModesPrinter(job['data']).process_image()
            r.set(jobkey, '1', 60 * 5)

def loop():
    while True:
        try:
            res = requests.get(ROOT_URL)
            process_jobs(res.json())
        except Exception as e:
            print('{} :: {}'.format(datetime.now().isoformat(), e))
        finally:
            sleep(10)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test = 'yuv.adm|062015|9A8D6D736489|eff51f2af82c06071120a'
        ModesPrinter(test).test_image()
    else:
        print('{} :: Startup'.format(datetime.now().isoformat()))
        loop()
