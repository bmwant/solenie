import os
from pathlib import Path

import settings
from jerry.nltk_rst import process_file_to_html


rst_path = '/home/user/.pr/nltk_book/book/ch03.rst'
BOOK_PATH = '/home/user/.pr/nltk_book/book'
OUT_DIRECTORY = settings.DATA_DIR / 'nltk_book_html'


def _convert_file(filepath: Path):
    filename, _ = os.path.splitext(filepath.name)
    out_filename = f'{filename}.html'
    out_filepath = OUT_DIRECTORY / out_filename
    print('Processing', filepath)
    process_file_to_html(filepath, out_filepath)


def convert_to_html():
    path = Path(BOOK_PATH)
    for item in path.glob('**/*.rst'):
        filename, ext = os.path.splitext(item.name)
        if filename.startswith('ch') and filename[-1].isdigit():
            _convert_file(item)


if __name__ == '__main__':
    # 04
    # 07
    # 08
    # 09
    # 10
    _convert_file(Path('/home/user/.pr/nltk_book/book/ch04.rst'))
    # convert_to_html()
