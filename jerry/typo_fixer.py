import os
import re
from pathlib import Path
from collections import defaultdict

from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn

import settings
from summer.tokenizer import tokenize
from jerry.nltk_rst import process_file_to_html


BOOK_PATH = Path('/home/user/.pr/nltk_book/book')
OUT_DIRECTORY = settings.DATA_DIR / 'nltk_book_html'
COMMENT_REGEX = re.compile(r'^<---.+--->$')



def _convert_file(filepath: Path):
    filename, _ = os.path.splitext(filepath.name)
    out_filename = f'{filename}.html'
    out_filepath = OUT_DIRECTORY / out_filename
    print('Processing', filepath)
    process_file_to_html(filepath, out_filepath)


def convert_to_html(path):
    for item in path.glob('**/*.rst'):
        filename, ext = os.path.splitext(item.name)
        if filename.startswith('ch') and filename[-1].isdigit():
            _convert_file(item)


def convert_to_raw_text(path):
    for item in path.glob('*.html'):
        filename, ext = os.path.splitext(item.name)
        out_filename = f'{filename}_raw.txt'
        text = get_text_from_html(item)
        out_filepath = OUT_DIRECTORY / out_filename
        print('Writing result to a file', out_filepath)
        with open(out_filepath, 'w') as f:
            f.write(text)


def get_text_from_html(path) -> str:
    print('Extracting raw text from', path)
    with open(path) as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html5lib')
    # Remove error messages
    error_block = soup.find('div', {'class': 'system-messages section'})
    error_block.extract()
    [x.extract()
     for x in soup.find_all('div', {'class': 'system-message'})]
    # Remove script tags
    [x.extract() for x in soup.find_all('script')]
    text = soup.get_text().split('\n')
    lines = [line for line in text if line.strip()]
    output = '\n'.join(filter(lambda l: not _ignore_line(l), lines))
    return output


def _ignore_line(line):
    if line.startswith('>>>'):
        return True

    if line.startswith('...'):
        return True

    if COMMENT_REGEX.match(line):
        return True

    return False


def _check_word(word, lang='eng'):
    # ignore stopwords once again
    if wn.synsets(word):
        return True
    return False


def _is_punct(token):
    return token in ['``', "''", '...', '']


def _is_name(token):
    return False


def _is_uri(token):
    return False


def _is_time(token):
    return False


def _is_code(token):
    return False


def check_text(text):
    stats = defaultdict(int)
    tokens = tokenize(text, language='english')
    for index, token in enumerate(tokens):
        if len(token) == 1:
            stats['one_letter'] += 1
            continue
        if _is_punct(token):
            stats['punctuation'] += 1
            continue
        if token.startswith("'"):
            token = token[1:]
            stats['quoted'] += 1
        if token.endswith("'"):
            token = token[:-1]
        if not _check_word(token):
            print(token)
    return stats


if __name__ == '__main__':
    # convert_to_html(BOOK_PATH)
    # convert_to_raw_text(OUT_DIRECTORY)
    txt_file = '/home/user/.pr/solenie/data/nltk_book_html/ch02_raw.txt'
    with open(txt_file) as f:
        print(check_text(f.read()))
