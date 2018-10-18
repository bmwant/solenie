from unittest import mock

import pytest

from jerry.proxy.base import BaseProxyPool
from jerry.proxy.file_pool import FileProxyPool
from jerry.proxy.scylla_pool import ScyllaProxyPool


@pytest.fixture
def patch_pools():
    """
    Reset pool classes to initial state that could have been touched
    with other tests previously
    """
    BaseProxyPool._proxies = None
    FileProxyPool._proxies = None
    ScyllaProxyPool._proxies = None


def test_subclasses_has_separate_proxy_stores(patch_pools):
    pool1 = FileProxyPool()
    pool2 = ScyllaProxyPool()

    proxies1 = ['http://41.55.44.71:3128/']
    proxies2 = ['http://42.55.44.72:3128/']
    with \
            mock.patch(
                'jerry.proxy.file_pool.FileProxyPool.load_proxies'
            ) as file_load_mock, \
            mock.patch(
                'jerry.proxy.scylla_pool.ScyllaProxyPool.load_proxies'
            ) as scylla_load_mock:
        file_load_mock.return_value = proxies1
        scylla_load_mock.return_value = proxies2

        p1 = pool1.proxies
        p2 = pool2.proxies
        p1_again = pool1.proxies

        assert p1 == p1_again
        assert p1 != p2
        assert pool1._proxies is not None
        assert pool2._proxies is not None
        assert pool1._proxies != pool2._proxies
        assert BaseProxyPool._proxies is None

        file_load_mock.assert_called_once()
        scylla_load_mock.assert_called_once()
