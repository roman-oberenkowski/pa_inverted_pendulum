class Pendulum:
    def __init__(self, mass, length, inertia):
        self._mass = mass
        self._length = length
        self._inertia = inertia

        return

    def mass(self):
        return self._mass

    def set_mass(self, mass):
        self._mass = mass
        return

    def length(self):
        return self._length

    def set_length(self, length):
        self._length = length
        return

    def inertia(self):
        return self._inertia

    def set_inertia(self, inertia):
        self._inertia = inertia
        return

