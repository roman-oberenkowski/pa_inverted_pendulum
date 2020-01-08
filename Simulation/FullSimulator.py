from Simulation import AbstractSimulator

class FullSimulator(AbstractSimulator.AbstractSimulator):
    def __init__(self, cart_mass, cart_rub, pendulum_mass, pendulum_length, pendulum_inertia,  x0, theta0, x, theta, g,
                 tp=0.01, tk=100):
        super().__init__(cart_mass, cart_rub, pendulum_mass, pendulum_length, pendulum_inertia, x0, theta0, x, theta, g)

        self.tp = tp
        self.tc = int(tk / tp)

        self.time = [0.0]
        self.location = [self.inverse_pendulum.location()]
        self.angle = [self.inverse_pendulum.angel()]

        return

    def simulate(self):
        for i in range(0, self.tc):
            e1 = self.theta - self.inverse_pendulum.angel()
            self.angle_regulator.calculate_step(e1, self.tp)
            u1 = self.angle_regulator.get_u()

            e2 = self.x - self.inverse_pendulum.location()
            self.location_regulator.calculate_step(e2, self.tp)
            u2 = self.location_regulator.get_u()

            u = u1 - u2

            self.inverse_pendulum.calculate(self.tp, u)
            temp_x = self.inverse_pendulum.location()
            temp_theta = self.inverse_pendulum.angel()

            self.time.append(self.time[-1] + self.tp)
            self.location.append(temp_x)
            self.angle.append(temp_theta)

        return

    def reset(self, cart_mass, cart_rub, pendulum_mass, pendulum_length, pendulum_inertia, x0, theta0, x, theta, g,
              tp=0.01, tk=100):
        super().reset(cart_mass, cart_rub, pendulum_mass, pendulum_length, pendulum_inertia, x0, theta0, x, theta, g)

        self.tp = tp
        self.tc = int(tk / tp)

        self.time = [0.0]
        self.location = [self.inverse_pendulum.location()]
        self.angle = [self.inverse_pendulum.angel()]

        return

    def get_result(self):
        return self.time, self.location, self.angle
