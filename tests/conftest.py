import asyncio

import attr
import pytest

import settings


TESTS_DIR = settings.PROJECT_ROOT / 'tests'
PAGES_DIR = TESTS_DIR / 'pages'


@pytest.fixture
def page_html():
    def inner(page_name):
        filename = f'{PAGES_DIR}/{page_name}.html'
        with open(filename) as f:
            return f.read()
    return inner


@pytest.fixture
def loop():
    loop_ = asyncio.new_event_loop()
    asyncio.set_event_loop(None)

    yield loop_

    if not loop_.is_closed():
        loop_.call_soon(loop_.stop)
        loop_.run_forever()
        loop_.close()


@pytest.fixture
def user():
    User = attr.make_class(
        'User',
        ['id', 'name', 'email', 'password', 'permissions']
    )
    return User(
        id=1,
        name='user',
        email='user@gmail.com',
        password='password',
        permissions='',
    )


@pytest.mark.tryfirst
def pytest_pyfunc_call(pyfuncitem):
    if 'run_loop' in pyfuncitem.keywords:
        funcargs = pyfuncitem.funcargs
        loop = funcargs['loop']
        testargs = {arg: funcargs[arg]
                    for arg in pyfuncitem._fixtureinfo.argnames}
        loop.run_until_complete(pyfuncitem.obj(**testargs))
        return True


def pytest_runtest_setup(item):
    if 'run_loop' in item.keywords:
        if 'loop' not in item.fixturenames:
            item.fixturenames.append('loop')

    if 'external' in item.keywords and \
            not item.config.getoption('--run-external'):
        pytest.skip('Need to specify --run-external to run tests that uses '
                    'external resources')


def pytest_addoption(parser):
    """
    Skip tests that rely on external resources unless explicitly specified.
    """
    parser.addoption('--run-external', action='store_true',
                     default=False,
                     help='Run tests that rely on external resources '
                          '(e.g. redis, web-sites)')
