from Objects import InversePendulum
from Regulators import PID


class System:
    def __init__(self, rangel: PID, rlocation: PID, inverse_pendulum: InversePendulum, x, theta,
                 tp=0.01, tk=100):
        self.rangel = rangel
        self.rlocation = rlocation
        self.inverse_pendulum = inverse_pendulum
        self.tp = tp
        self.tc = int(tk / tp)
        self.x = x
        self.theta = theta
        self.time = [0.0]
        self.location = [self.inverse_pendulum.location()]
        self.angel = [self.inverse_pendulum.angel()]

        return

    def simulate(self):
        for i in range(0, self.tc):
            e1 = self.theta - self.inverse_pendulum.angel()
            self.rangel.calculate(e1, self.tp)
            u1 = self.rangel.get_u()

            e2 = self.x - self.inverse_pendulum.location()
            self.rlocation.calculate(e2, self.tp)
            u2 = self.rlocation.get_u()

            u = u1 - u2

            self.inverse_pendulum.calculate(self.tp, u)
            temp_x = self.inverse_pendulum.location()
            temp_theta = self.inverse_pendulum.angel()

            self.time.append(self.time[-1] + self.tp)
            self.location.append(temp_x)
            self.angel.append(temp_theta)

        return

    def get_result(self):
        return self.time, self.location, self.angel
