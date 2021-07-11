from enum import Enum


class Mode(Enum):
    COOL = 1
    HEAT = 2


class State(Enum):
    ACTING = 1
    STOP = 2


class AirConditioner:
    def __init__(self, Tr, Tac, Tout, k, kac, Tc_low, Tc_high, mode):
        """
        :param Tr: room temperature - float
        :param Tac: coils' temperature - int
        :param Tout: outside air temperature - int
        :param k, kac: cooling coefficients - float
        :param Tc_low, Tc_high: control temperature - int
        """
        if k < 0 or kac < 0:
            print("Please check cooling coefficients' coherence.")
            return
        if Tc_low > Tc_high:
            print("Please check control temperature coherence.")
            return
        self.Tac = Tac
        self.Tout = Tout
        self.k = k
        self.kac = kac
        self.period_clock = -1
        self.period = -1
        self.last_start_moment = 0
        self.action_time = 0
        self.Tc_low = Tc_low
        self.Tc_high = Tc_high
        self.mode = mode
        if mode == Mode.COOL:
            if Tr > Tc_low:
                self.state = State.ACTING
            else:
                self.state = State.STOP
        else:
            if Tr < Tc_high:
                self.state = State.ACTING
            else:
                self.state = State.STOP

    def act(self, t, Tr):
        """
        :param t: time - float
        :param Tr: room temperature - float
        :return: dTr/dt - float
        """
        if self.mode == Mode.COOL:
            if self.state == State.ACTING:
                if Tr <= self.Tc_low:
                    self.state = State.STOP
                    self.action_time += t - self.last_start_moment
                    if self.period == -1:
                        if self.period_clock == -1:
                            self.period_clock = t
                        else:
                            self.period = t - self.period_clock
                    return self.k * (self.Tout - Tr)
                return self.k * (self.Tout - Tr) + self.kac * (self.Tac - Tr)
            if Tr > self.Tc_high:
                self.state = State.ACTING
                self.last_start_moment = t
                return self.k * (self.Tout - Tr) + self.kac * (self.Tac - Tr)
            return self.k * (self.Tout - Tr)
        if self.state == State.ACTING:
            if Tr >= self.Tc_high:
                self.state = State.STOP
                self.action_time += t - self.last_start_moment
                if self.period == -1:
                    if self.period_clock == -1:
                        self.period_clock = t
                    else:
                        self.period = t - self.period_clock
                return self.k * (self.Tout - Tr)
            return self.k * (self.Tout - Tr) + self.kac * (self.Tac - Tr)
        if Tr < self.Tc_low:
            self.state = State.ACTING
            self.last_start_moment = t
            return self.k * (self.Tout - Tr) + self.kac * (self.Tac - Tr)
        return self.k * (self.Tout - Tr)

    def act_t(self, t, Tr):
        """
        :param t: time - float
        :param Tr: room temperature - float
        :return: 0
        """
        return 0

    def act_y(self, t, Tr):
        """
        :param t: time - float
        :param Tr: room temperature - float
        :return: dTr/dt - float
        """
        if self.mode == Mode.COOL:
            if self.state == State.ACTING:
                if Tr <= self.Tc_low:
                    self.state = State.STOP
                    return -self.k
                return -self.k - self.kac
            if Tr > self.Tc_high:
                self.state = State.ACTING
                return -self.k - self.kac
            return -self.k
        if self.state == State.ACTING:
            if Tr >= self.Tc_high:
                self.state = State.STOP
                return -self.k
            return -self.k - self.kac
        if Tr < self.Tc_low:
            self.state = State.ACTING
            return -self.k - self.kac
        return -self.k

    def get_period(self):
        return self.period

    def get_action_time(self):
        return self.action_time
