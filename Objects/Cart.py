class Cart:
    def __init__(self, mass, rub):
        self._mass = mass
        self._rub = rub

        return

    def mass(self):
        return self._mass

    def set_mass(self, mass):
        self._mass = mass
        return

    def rub(self):
        return self._rub

    def set_rub(self, rub):
        self._rub = rub
        return
