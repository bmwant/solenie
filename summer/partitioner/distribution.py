import math

from buttworld.logger import get_logger


class DistributionPartitioner(object):
    def __init__(self, data, pred, ratio=0.85):
        self.data = data
        self.pred = pred
        self.ratio = ratio
        self._training_data = None
        self._test_data = None
        self.logger = get_logger(self.__class__.__name__.lower())

    # todo (misha): write it in a good way please
    def partition(self):
        len_pos = len(list(filter(self.pred, self.data)))
        len_neg = len(self.data) - len_pos
        len_pos_training = math.floor(len_pos*self.ratio)
        len_neg_training = math.floor(len_neg*self.ratio)

        pos_ = 0
        neg_ = 0
        partition_training = []
        partition_test = []
        for item in self.data:
            if self.pred(item):
                if pos_ < len_pos_training:
                    partition_training.append(item)
                    pos_ += 1
                else:
                    partition_test.append(item)
            else:
                if neg_ < len_neg_training:
                    partition_training.append(item)
                    neg_ += 1
                else:
                    partition_test.append(item)

        self.logger.info(
            'Created train partition(%s) and test partition(%s)',
            len(partition_training), len(partition_test)
        )
        self._training_data = partition_training
        self._test_data = partition_test

    @property
    def training_data(self):
        if self._training_data is None:
            raise RuntimeError('You forgot to call `partition` method')
        return self._training_data

    @property
    def test_data(self):
        if self._test_data is None:
            raise RuntimeError('You forgot to call `partition` method')
        return self._test_data
