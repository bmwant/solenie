from dp import fill_memory, resolve


def test_correct_values():
    """
    4 - 83.505
    3 - 77.143
    2 - 69.231
    1 - 60.0
    # use later
    1 0.6
    2 0.648
    3 0.68256
    4 0.710208
    """
    bounds = (
        (59.9, 60.1),
        (69.230, 69.232),
        (77.142, 77.144),
        (83.504, 83.506),
    )
    p = 0.6
    for i, (lower, upper) in enumerate(bounds, start=1):
        fill_memory(i, p)
        pn = resolve(i)
        assert lower < pn*100 < upper
