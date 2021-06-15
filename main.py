from air_conditioner import AirConditioner, Mode
from methods import euler, taylor2, trapezium, mean, rk4
import matplotlib.pyplot

Tac = 35
Tout = 15
k = 0.03
kac = 0.1
Tc_low = 22
Tc_high = 24

Tr = 18
tf = 100
n = 500

airConditioner = AirConditioner(Tr, Tac, Tout, k, kac, Tc_low, Tc_high, Mode.HEAT)

# t, Trk4 = rk4(airConditioner.act, 0, tf, n, Tr)
t, T = trapezium(airConditioner.act, 0, tf, n, Tr)

matplotlib.pyplot.plot(t, T, label="Test")
matplotlib.pyplot.title('Air conditioning a room')
matplotlib.pyplot.xlabel('t')
matplotlib.pyplot.ylabel('room temperature')
matplotlib.pyplot.legend()
matplotlib.pyplot.show()
