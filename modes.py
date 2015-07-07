import cups

PRINTER = 'Canon_iP7200_series'


def print():
    conn = cups.Connection()
    conn.printFile(PRINTER, 'base.jpg', 'title', {})
