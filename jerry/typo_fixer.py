import os
from pathlib import Path


rst_path = '/home/user/.pr/nltk_book/book/ch03.rst'
BOOK_PATH = '/home/user/.pr/nltk_book/book'
OUT_DIRECTORY = ''


def _convert_file(filepath):
    pass


def convert_to_html():
    path = Path(BOOK_PATH)
    for item in path.glob('**/*.rst'):
        filename, ext = os.path.splitext(item.name)
        if filename.startswith('ch') and filename[-1].isdigit():
            print(filename)
            _convert_file(item)


if __name__ == '__main__':
    convert_to_html()



