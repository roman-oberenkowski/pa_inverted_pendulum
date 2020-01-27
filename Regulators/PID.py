from Regulators import AbstractRegulator


class PID(AbstractRegulator.AbstractRegulator):
    def __init__(self, kp, ti, td, tp, windup_guard=50, e0=0, x0=0):
        super().__init__(tp)
        self.kp = kp
        self.ti = ti
        self.td = td

        self.PTerm = 0
        self.ITerm = 0
        self.DTerm = 0

        self.windup_guard = windup_guard
        self.last_e = e0

        self.u = 0

        return

    def calculate_step(self, e, tp):
        self.PTerm = e
        self.ITerm += self.tp / self.ti * e
        self.DTerm = (e - self.last_e) / self.tp

        if self.ITerm < -self.windup_guard:
            self.ITerm = -self.windup_guard
        elif self.ITerm > self.windup_guard:
            self.ITerm = self.windup_guard

        self.u = self.kp * (self.PTerm + self.ITerm + self.DTerm * self.td)

        self.last_e = e

        return

    def reset(self, e0=0):
        self.PTerm = 0
        self.ITerm = 0
        self.DTerm = 0

        self.last_e = e0

        return

    def get_u(self):
        return self.u
