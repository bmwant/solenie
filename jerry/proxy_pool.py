

"""
* aiohttp.client_exceptions.ClientHttpProxyError: 500, message='Internal Server Error'
* aiohttp.client_exceptions.ClientProxyConnectionError: Cannot connect to host 78.159.79.245:57107
  ssl:None [Connect call failed ('78.159.79.245', 57107)]

* <asyncio.sslproto.SSLProtocol object at 0x7f3afe19b4a8> stalled during handshake
Traceback (most recent call last):
  File "grab_data.py", line 39, in <module>
    loop.run_until_complete(main())
  File "/usr/local/lib/python3.7/asyncio/base_events.py", line 566, in run_until_complete
    return future.result()
  File "grab_data.py", line 30, in main
    reviews = list(chain.from_iterable(await asyncio.gather(*tasks)))
  File "/usr/local/lib/python3.7/asyncio/tasks.py", line 570, in _wrap_awaitable
    return (yield from awaitable.__await__())
  File "/home/user/.pr/solenie/jerry/crawler/base.py", line 32, in process
    async for page in self.get_next_page():
  File "/home/user/.pr/solenie/jerry/crawler/base.py", line 18, in get_next_page
    page_html = await self.fetcher.get(url)
  File "/home/user/.pr/solenie/jerry/fetcher.py", line 12, in get
    async with session.get(url, proxy=proxy) as response:
  File "/home/user/.virtualenvs/solenie/lib/python3.7/site-packages/aiohttp/client.py", line 855, in __aenter__
    self._resp = await self._coro
  File "/home/user/.virtualenvs/solenie/lib/python3.7/site-packages/aiohttp/client.py", line 377, in _request
    tcp_nodelay(conn.transport, True)
  File "/home/user/.virtualenvs/solenie/lib/python3.7/site-packages/aiohttp/tcp_helpers.py", line 32, in tcp_nodelay
    sock = transport.get_extra_info('socket')
AttributeError: 'NoneType' object has no attribute 'get_extra_info'
"""
