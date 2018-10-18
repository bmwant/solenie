from unittest import mock

import pytest

from jerry.proxy_pool import ProxyPool
from tests.helpers import AsyncMock


@pytest.fixture
def patch_pool():
    with mock.patch('jerry.proxy_pool.ProxyPool._check_proxy',
                    AsyncMock) as check_mock:
        check_mock.return_value = True
        yield


@pytest.mark.run_loop
async def test_get_proxy_return_new_proxy(patch_pool):
    pool = ProxyPool()

    p1 = await pool.get_proxy()
    p2 = await pool.get_proxy()

    assert p1 != p2


@pytest.mark.run_loop
async def test_iterating_yields_new_proxy(patch_pool):
    pool = ProxyPool()
    proxies = set()

    counter = 0
    async for proxy in pool:
        proxies.add(proxy)
        new_proxy = await pool.get_proxy()
        assert new_proxy != proxy
        proxies.add(new_proxy)
        counter += 1
        if counter > 3:
            break

    assert len(proxies) == 2*counter


@pytest.mark.run_loop
async def test_does_not_raise_stop_iteration(patch_pool):
    pool = ProxyPool()
    proxies = set()

    iterations = 2*len(pool)
    for i in range(iterations):
        next_proxy = await pool.get_proxy()
        assert isinstance(next_proxy, str)
        proxies.add(next_proxy)

    assert len(proxies) == len(pool)


def test_load_proxies_just_once():
    proxies = [
        'http://41.55.44.76:3128/',
        'http://41.55.44.77:3128/',
        'http://41.55.44.78:3128/',
    ]
    with mock.patch('jerry.proxy_pool.ProxyPool.load_proxies',
                    return_value=proxies) as load_mock:
        pool1 = ProxyPool()
        pool2 = ProxyPool()
        p1 = pool1.proxies
        p2 = pool2.proxies
        assert ProxyPool._proxies is not None
        assert pool1._proxies == pool2._proxies
        assert p1 != p2
        assert load_mock.called
        assert load_mock.call_count == 1
