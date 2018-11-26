import os
from pathlib import Path
from collections import defaultdict

import click
from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords, words

import settings
from summer.tokenizer import tokenize
from jerry.checker import checks
from jerry.checker.checks import DoNotCheck
from jerry.checker.nltk_rst import process_file_to_html


BOOK_PATH = Path('/home/user/.pr/nltk_book/book')
OUT_DIRECTORY = settings.DATA_DIR / 'nltk_book_html'


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
    output = '\n'.join(filter(lambda l: not checks._is_prompt(l), lines))
    return output


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


def check_text(text, verbose=True):
    unknown = defaultdict(list)
    stats = defaultdict(int)
    tokens = tokenize(text, language='english')
    testers = (
        ('one_letter', checks._is_one_letter),
        ('punctuation', checks._is_punct),
        ('uri', checks._is_uri),
        ('time', checks._is_time),
        ('code', checks._is_code),
        ('name', checks._is_name),
        ('variable', checks._is_variable),
        ('number',checks._is_number),
        ('aux', checks._is_aux),
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
                unknown[token].append(index)

    if verbose:
        for elem, idx in unknown.items():
            if len(idx) > 2:
                continue
            for index in idx:
                print_unknown_context(elem, index, tokens)

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


def _check_raw_file(filepath):
    with open(filepath) as f:
        text = f.read()
        click.secho(f'Unknown words in file {filepath.name}:', fg='yellow')
        stats = check_text(text)
        for key, value in stats.items():
            print(f'{key} = {value}')


def check_raw_files(path):
    for item in sorted(path.glob('*.txt')):
        _check_raw_file(item)


if __name__ == '__main__':
    # Step 1.
    # convert_to_html(BOOK_PATH)
    # Step 2.
    # convert_to_raw_text(OUT_DIRECTORY)
    # Step 3.
    # check_raw_files(OUT_DIRECTORY)
    _check_raw_file(OUT_DIRECTORY / 'ch03_raw.txt')
