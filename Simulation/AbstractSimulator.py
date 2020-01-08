from Objects import Cart, Pendulum, InversePendulum
from Regulators import AbstractRegulator, PID
import math


class AbstractSimulator:
    def __init__(self, cart_mass, cart_rub, pendulum_mass, pendulum_length, pendulum_inertia, x0, theta0, x, theta, g):
        cart = Cart.Cart(cart_mass, cart_rub)
        pendulum = Pendulum.Pendulum(pendulum_mass, pendulum_length, pendulum_inertia)

        self.inverse_pendulum = InversePendulum.InversePendulum(cart, pendulum, g, x0, theta0)

        self.angle_regulator = PID.PID(-50.8, 7.26, 0.24, 0.1)
        self.location_regulator = PID.PID(6, math.inf, 1.5, 0.1)
        self.x = x
        self.theta = theta

        return

    def reset(self, cart_mass, cart_rub, pendulum_mass, pendulum_length, pendulum_inertia, x0, theta0, x, theta, g):
        self.inverse_pendulum.cart.set_mass(cart_mass)
        self.inverse_pendulum.cart.set_rub(cart_rub)
        self.inverse_pendulum.set_g(g)
        self.inverse_pendulum.pendulum.set_mass(pendulum_mass)
        self.inverse_pendulum.pendulum.set_length(pendulum_length)
        self.inverse_pendulum.pendulum.set_inertia(pendulum_inertia)
        self.inverse_pendulum.pendulum.set_location(x0)
        self.inverse_pendulum.pendulum.set_angel(theta0)
        self.x = x
        self.theta = theta

        self.inverse_pendulum.update_matrix()

        self.angle_regulator.reset()
        self.location_regulator.reset()

        return

    def simulate(self):
        pass

    def get_result(self):
        pass
