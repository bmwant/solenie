import sys
# for jupyter to work here
sys.path.append('/Users/misha/projects/solenie')


import matplotlib.pyplot as plt
import numpy as np

from jerry.client import get_client


client = get_client('kuna')
symbol = 'DOGEUAH'
volume_uah = lambda x: x[0]*x[1]
volume_doge = lambda x: x[1]
"""
[[8.61, -6163.0911, 3],
 [8.62, -16940.203, 1],
 [8.66, -9.98, 1],
 [8.67, -0.0001, 1],
 [8.68, -0.0008, 2],
 [8.7, -1.0, 1]]
"""


def get_volume_doge():
    ask = client.get_ask(symbol)
    bid = client.get_bid(symbol)
    bid_volume = sum(map(volume_doge, bid))
    ask_volume = abs(sum(map(volume_doge, ask)))
    return {
        'bid': bid_volume,
        'ask': ask_volume,
    }


def get_volume_uah():
    ask = client.get_ask(symbol)
    bid = client.get_bid(symbol)
    bid_volume = sum(map(volume_uah, bid))
    ask_volume = abs(sum(map(volume_uah, ask)))
    return {
        'bid': bid_volume,
        'ask': ask_volume,
    }


def graph_volume(volume, ylabel=''):
    fig, ax = plt.subplots()
    ax.bar(0, volume['bid'], color='green')
    ax.bar(1, volume['ask'], color='red')
    labels = ['bid', 'ask']
    x = np.arange(len(labels))
    ax.set_xticks(x)
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(labels)
    plt.show()