import time
import hmac
import json
import hashlib
import operator
from urllib.parse import urljoin

import requests

from trader import config
from trader.logger import logger
from trader.client.base import BaseClient


class KunaClient(BaseClient):
    def __init__(self):
        super().__init__(name='KunaClient')

    def get_tickers(self, symbols):
        """
        [[
            'btcuah',  # symbol
            1218197.0,  # price BID
            22388092.0,  # orderbook volume BID
            1225367.0,  # price ASK
            8.250932,  # ordrebook volume ASK
            20264.0,  # 24h price change absolute
            -1.63,  # 24h price change percent
            1225358.0,  # last price
            11.3107,  # trading volume
            1263922.0,  # 24h max price
            1190000.0  # 24h min price
        ]]
        """
        url = urljoin(config.KUNA_API_BASE, f'/v3/tickers?symbols={symbols}')
        r = requests.get(url)
        return r.json()

    def get_ask(self, symbol):
        """
        [[1278215.0, -0.004554, 1], [1278225.0, -0.002557, 1], [1283674.0, -0.01281, 1]
        """
        url = urljoin(config.KUNA_API_BASE, f'/v3/book/{symbol}')
        r = requests.get(url)
        data = r.json()
        ask = list(filter(lambda x: x[1] < 0, data))
        return ask

    def get_bid(self, symbol):
        url = urljoin(config.KUNA_API_BASE, f'/v3/book/{symbol}')
        r = requests.get(url)
        data = r.json()
        bid = list(filter(lambda x: x[1] > 0, data))
        return bid

    def get_acc_balance(self):
        return self._signed_request('/v3/auth/r/wallets', '')

    def get_orders_hist(self):
        return self._signed_request('/v3/auth/r/orders/hist', {})

    def make_order(self, symbol, amount: float):
        """
        [
            687842465,  # order id
            None, None,
            'btcuah',  # symbol
            1613053188000,  # create time
            1613053188000,  # update time
            '-0.000005',  # initial volume
            '0.000005',  # volume
            'LIMIT',  # order type
            None, None, None, None,
            'ACTIVE',
            None, None,
            '1227777.0',
            '0.0',
            None, None, None, None, None, None, None, None, None, None, None, None, None, None
        ]
        """
        body = {
            'symbol': symbol,
            'type': 'market',  #'limit',
            'amount': amount,
            # 'price': price, required for limit only
        }
        # logger.info(body)
        return self._signed_request('/v3/auth/w/order/submit', body)

    def _signed_request(self, api_path, data):
        nonce = round(time.time() * 1000)
        body = json.dumps(data, separators=(',', ':'))
        signature_string = f'{api_path}{nonce}{body}'
        signature = hmac.new(
            config.KUNA_SECRET_KEY.encode(),
            signature_string.encode(),
            hashlib.sha384
        ).hexdigest()
        headers = {
            'accept': 'application/json',
            'kun-nonce': str(nonce),
            'kun-apikey': config.KUNA_API_KEY,
            'kun-signature': signature
        }

        url = urljoin(config.KUNA_API_BASE, api_path)
        r = requests.post(url, headers=headers, data=body)
        return r.json()