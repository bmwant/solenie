import re

from nltk.corpus import names


COMMENT_REGEX = re.compile(r'^<---.+--->$')
TIME_REGEX = re.compile(r'\d{2}:\d{2}:\d{2}')
VARIABLE_REGEX = re.compile(r'[a-zA-Z]{1,2}\d{1,2}')
NUM1_REGEX = re.compile(r'\d+[kK]?\+?')
NUM2_REGEX = None


class DoNotCheck(ValueError):
    """No need to check the word further"""


def _is_prompt(line):
    if line.startswith('>>>'):
        return True

    if line.startswith('...'):
        return True

    if COMMENT_REGEX.match(line):
        return True

    return False


def _is_punct(token):
    # single quotes might be removed at this time, just for a confidence
    return token in ['', '``', "''", '...', '***']


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


def _is_number(token):
    n_token = token.replace('.', '').replace(',', '')
    return NUM1_REGEX.match(n_token)


def _is_one_letter(token):
    return len(token) == 1


def _is_aux(token):
    aux_keywords = (
        'et',
        'al',
        'etc',
        'n\'t',
    )
    return token in aux_keywords


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
        'startswith',
    )
    for char in code_chars:
        if char in token:
            return True

    return token in code_keywords
