import numpy as np
from Objects import Cart, Pendulum


class InversePendulum:
    def __init__(self, cart, pendulum, g, x0=0, theta0=0):
        # parametry układu
        self.cart = cart
        self.pendulum = pendulum
        self.g = g

        # zmienne pomocnicze
        self.v = 0
        self.a = 0
        self.omega = 0
        self.epsilon = 0

        self.update_matrix()

        # zmienne stanu układu
        self.x = x0
        self.theta = theta0

        return

    def calculate(self, tp, force):
        x = np.array([[self.omega, self.theta, self.v, self.x]]).T

        A = np.dot(self.A, x)
        B = self.B * force

        dx = A + B

        self.omega = dx[1][0] + tp * self.epsilon
        self.epsilon = dx[0][0]
        self.v = dx[3][0] + tp * self.a
        self.a = dx[2][0]

        self.theta = self.theta + tp * self.omega
        self.x = self.x + tp * self.v

        return

    def location(self):
        return self.x

    def angel(self):
        return self.theta

    def set_cart(self, cart: Cart):
        self.cart = cart
        return

    def set_pendulum(self, pendulum: Pendulum):
        self.pendulum = pendulum
        return

    def set_location(self, x0):
        self.x = x0
        return

    def set_angel(self, theta0):
        self.theta = theta0
        return

    def set_g(self, g):
        self.g = g
        return

    def update_matrix(self):
        self.A = np.array([[0, (self.pendulum.mass() + self.cart.mass()) * self.g /
                       (self.cart.mass() * self.pendulum.length() / 2),
                       self.cart.rub() / (self.cart.mass() * self.pendulum.length() / 2), 0],
                      [1, 0, 0, 0],
                      [0, -self.pendulum.mass() * self.g / self.cart.mass(), -self.cart.rub() / self.cart.mass(), 0],
                      [0, 0, 1, 0]])
        self.B = np.array([[-1 / (self.cart.mass() * self.pendulum.length() / 2), 0, 1 / self.cart.mass(), 0]]).T
        return
