# tests/test_moving_average.py

from crawler.moving_average import MovingAverage

def test_moving_average_basic():
    ma = MovingAverage(window_size=3)
    assert ma.update(10) == 10
    assert ma.update(20) == 15
    assert ma.update(30) == 20
    assert ma.update(40) == 30  # Oldest (10) is dropped
