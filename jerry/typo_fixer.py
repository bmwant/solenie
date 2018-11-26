import os
import re
from pathlib import Path
from collections import defaultdict, Counter

import click
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from nltk.corpus import names, stopwords, words

import settings
from summer.tokenizer import tokenize
from jerry.nltk_rst import process_file_to_html


BOOK_PATH = Path('/home/user/.pr/nltk_book/book')
OUT_DIRECTORY = settings.DATA_DIR / 'nltk_book_html'
COMMENT_REGEX = re.compile(r'^<---.+--->$')
TIME_REGEX = re.compile(r'\d{2}:\d{2}:\d{2}')
VARIABLE_REGEX = re.compile(r'[a-zA-Z]{1,2}\d{1,2}')



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


def _check_word_wrapper():
    vocab = set(w.lower() for w in words.words())

    def check_word(word, lang='eng'):
        # ignore stopwords once again
        if word in stopwords.words('english'):
            return True
        if wn.synsets(word):
            return True
        if word in vocab:
            return True
        return False

    return check_word

_check_word = _check_word_wrapper()


def _is_punct(token):
    # single quotes might be removed at this time, just for a confidence
    return token in ['', '``', "''", '...']


def _is_name_wrapper():
    all_names = [name.lower() for name in names.words('male.txt')] + \
                [name.lower() for name in names.words('female.txt')]

    def is_name(token):
        return token in all_names

    return is_name

_is_name = _is_name_wrapper()


def _is_uri(token):
    return token.startswith('//')


def _is_time(token):
    return TIME_REGEX.match(token)


def _is_variable(token):
    return VARIABLE_REGEX.match(token)


def _is_digit(token):
    return False


def _is_one_letter(token):
    return len(token) == 1


def _is_aux(token):
    # et
    # al
    # etc
    # n't
    return False


def _is_code(token):
    code_chars = ('_', '=', '.', '/', '\\')
    code_keywords = (
        'nltk',
        'def',
        'keyword',
        'elif',
        'endswith',
        'zipf',
        'dir',
        'api',
        'xml',
        'cfd',
        'cfdist',
        'freqdist',
        'latin1',
        'fileids',
        'abspath',
        'howto',
        'utf8',
        'dict',
        'iso',
        'traceback',
        'keyerror',
        'indexerror',
        'toolkit',
        'tokenize',
        'fileid',
        'misc',
    )
    for char in code_chars:
        if char in token:
            return True

    return token in code_keywords


class DoNotCheck(ValueError):
    """No need to check the word further"""


def check_text(text):
    unknown = Counter()
    stats = defaultdict(int)
    tokens = tokenize(text, language='english')
    testers = (
        ('one_letter', _is_one_letter),
        ('punctuation', _is_punct),
        ('uri', _is_uri),
        ('time', _is_time),
        ('code', _is_code),
        ('name', _is_name),
        ('variable', _is_variable),
    )
    for index, token in enumerate(tokens):
        # because of default nltk tokenization
        if token.startswith("'"):
            token = token[1:]
            stats['quoted'] += 1
        if token.endswith("'"):
            token = token[:-1]

        try:
            for key, tester in testers:
                if tester(token):
                    stats[key] += 1
                    raise DoNotCheck('Test passed')
        except DoNotCheck:
            continue

        for word in token.split('-'):
            if not _check_word(word):
                stats['unknown'] += 1
                print_unknown_context(token, index, tokens)
    return stats


def print_unknown_context(token, index, tokens):
    token_p, token_pp = '', ''
    token_n, token_nn = '', ''
    if index - 2 >= 0:
        token_pp = tokens[index-2]
    if index - 1 >= 0:
        token_p = tokens[index-1]

    if index + 1 < len(tokens):
        token_n = tokens[index+1]
    if index + 2 < len(tokens):
        token_nn = tokens[index+2]

    click.echo('{} {} {} {} {}'.format(
        token_pp,
        token_p,
        click.style(token, fg='red', bold=True),
        token_n,
        token_nn,
    ))

if __name__ == '__main__':
    # convert_to_html(BOOK_PATH)
    # convert_to_raw_text(OUT_DIRECTORY)
    txt_file = '/home/user/.pr/solenie/data/nltk_book_html/ch02_raw.txt'
    with open(txt_file) as f:
        print(check_text(f.read()))
