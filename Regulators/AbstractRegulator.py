import time


class AbstractRegulator:
    def __init__(self, tp):
        self.tp = tp

        self.last_time = time.time()

        return

    def calculate_real_time(self, e):
        actual_time = time.time()
        delta_time = self.last_time = actual_time

        if delta_time >= self.tp:
            self.calculate_step(e, delta_time)

            self.last_time = actual_time

        return

    def calculate_step(self, e, tp):
        pass

    def reset(self):
        pass

    def get_u(self):
        pass
