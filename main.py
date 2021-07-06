from air_conditioner import AirConditioner, Mode
from methods import euler, taylor2, trapezium, mean, rk4, rkf, pc
import matplotlib.pyplot

Tac = 35  # The temperature of the coils
Tout = 15  # The temperature of the outside air
k = 0.03  # cooling coefficient(wall)
kac = 0.1  # cooling coefficient(coils)
Tc_low = 22  # control temperature(low)
Tc_high = 24  # control temperature(high)

Tr = 18  # initial room temperature
tf = 100  # time extension for analysis
n = 500  # step number

airConditioner = AirConditioner(Tr, Tac, Tout, k, kac, Tc_low, Tc_high, Mode.HEAT)

t, Teuler = euler(airConditioner.act, 0, tf, n, Tr)
# t, Ttaylor2 = taylor2(airConditioner.act, airConditioner.act_t, airConditioner.act_y, 0, tf, n, Tr)
# t, Ttrapezium = trapezium(airConditioner.act, 0, tf, n, Tr)
# t, Tmean = mean(airConditioner.act, 0, tf, n, Tr)
t, Trk4 = rk4(airConditioner.act, 0, tf, n, Tr)
# trkf, Trkf = rkf(airConditioner.act, 0, tf, Tr, 0.1, 0.1, 0.01)
t, Tpc = pc(airConditioner.act, 0, tf, n, Tr)

matplotlib.pyplot.plot(t, Teuler, label="Euler")
# matplotlib.pyplot.plot(t, Ttaylor2, label="Taylor2")
# matplotlib.pyplot.plot(t, Ttrapezium, label="Trapezium")
# matplotlib.pyplot.plot(t, Tmean, label="Mean")
matplotlib.pyplot.plot(t, Trk4, label="Runge-Kutta4")
# matplotlib.pyplot.plot(trkf, Trkf, label="Runge-Kutta-Fehlberg")
matplotlib.pyplot.plot(t, Tpc, label="predictor-corrector")

matplotlib.pyplot.grid()
matplotlib.pyplot.title('Air conditioning a room')
matplotlib.pyplot.xlabel('t')
matplotlib.pyplot.ylabel('room temperature')
matplotlib.pyplot.legend()

matplotlib.pyplot.savefig('fig.eps')
matplotlib.pyplot.show()
