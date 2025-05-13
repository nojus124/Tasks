# crawler/moving_average.py

from collections import deque

class MovingAverage:
    def __init__(self, window_size):
        self.prices = deque(maxlen=window_size)

    def update(self, price):
        self.prices.append(price)
        return self.calculate()

    def calculate(self):
        if not self.prices:
            return None
        return sum(self.prices) / len(self.prices)
