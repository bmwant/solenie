from io import StringIO
from pathlib import Path

from docutils import frontend, utils
from docutils.parsers import rst

from jerry import nltk_rst
# from jerry.directives import strip_doctest_directives


def parse_rst(fileobj):
    default_settings = frontend.OptionParser(
        components=(rst.Parser,)).get_default_values()
    document = utils.new_document(fileobj.name, default_settings)
    parser = rst.Parser()
    text = fileobj.read()
    text = nltk_rst.strip_doctest_directives(text)
    parser.parse(text, document)


rst_path = '/home/user/.pr/nltk_book/book/ch04.rst'


def main():
    path = Path('/home/user/.pr/nltk_book/book')
    # for item in path.glob('**/*.rst'):
    #     print(item)

    with open(rst_path) as f:
        parse_rst(f)


if __name__ == '__main__':
    main()



