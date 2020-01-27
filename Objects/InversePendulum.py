import numpy as np
from math import pi

from Objects import Cart, Pendulum


class Angle:
    def __init__(self, alpha: float):
        self.angle = alpha
        self.normalize()

    def __add__(self, other: float):
        self.angle += other
        self.normalize()

        return self

    def __sub__(self, other: float):
        self.angle -= other
        self.normalize()

        return self

    def __mul__(self, other: float):
        self.angle *= other
        self.normalize()

        return self

    def __truediv__(self, other: float):
        self.angle /= other
        self.normalize()

        return self

    def normalize(self):
        self.angle = (self.angle + pi) % (2 * pi) - pi

    def __float__(self):
        return self.value()

    def value(self):
        return self.angle

    def set_value(self, value):
        self.angle = value

        self.normalize()


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

        # zmienne stanu układu
        self.x = x0
        self.theta = Angle(theta0)

        self.update_matrix()

        return

    def calculate(self, tp, force):
        X0 = np.array([[self.omega, self.theta.value(), self.v, self.x]]).T

        dX = np.dot(self.A, X0) + self.B * force

        X = X0 + dX * tp

        self.omega = X[0][0]
        self.theta.set_value(X[1][0])
        self.v = X[2][0]
        self.x = X[3][0]

        return

    def location(self):
        return self.x

    def angel(self):
        return self.theta.value()

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
        self.theta.set_value(theta0)
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
        self.C = np.array([[0, 1, 0, 0],
                           [0, 0, 0, 1]])
        self.D = np.array([[0, 0]]).T

        self.system = ss(self.A, self.B, self.C, self.D)

        return

    def get_matrix(self):
        return self.A, self.B, self.C, self.D
