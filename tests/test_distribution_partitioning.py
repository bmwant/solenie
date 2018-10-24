from summer.partitioner import DistributionPartitioner


def test_numbers_partitioning():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    def pred(item):
        return item % 2 == 0

    p = DistributionPartitioner(data, pred=pred, ratio=0.8)
    p.partition()

    assert len(p.training_data) == 8
    assert len(p.test_data) == 2

    assert p.training_data == [1, 2, 3, 4, 5, 6, 7, 8]
    assert p.test_data == [9, 0]
