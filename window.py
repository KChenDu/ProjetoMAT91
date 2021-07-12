from enum import Enum


class Integrator(Enum):
    EULER = 1
    TAYLOR2 = 2
    TRAPEZIUM = 3
    MEAN = 4
    RK4 = 5
    RKF = 6
    PC = 7
    COUNT = 8


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from air_conditioner import AirConditioner, Mode
from methods import euler, taylor2, trapezium, mean, rk4, rkf, pc

def create_param_spin(title, initial, callback, increment):
    adjustment = Gtk.Adjustment(upper=2000, step_increment=increment, page_increment=1)
    box_param = Gtk.Box()
    box_param.set_homogeneous(True)

    param_label = Gtk.Label(label=title)
    param_label.set_justify(Gtk.Justification.LEFT)
    param_label.set_halign(Gtk.Align.START)
    box_param.pack_start(param_label, True, True, 0)
    param_spin_button = Gtk.SpinButton()
    param_spin_button.set_adjustment(adjustment)
    param_spin_button.set_numeric(True)
    param_spin_button.set_digits(5)
    param_spin_button.set_value(initial)
    param_spin_button.connect("value-changed", callback)
    box_param.pack_start(param_spin_button, True, True, 0)

    return box_param

def create_integrator_type_checkbox(title, callback):
    box = Gtk.Box()
    box.set_homogeneous(True)
    label = Gtk.Label(label=title)
    label.set_justify(Gtk.Justification.LEFT)
    label.set_halign(Gtk.Align.START)
    box.pack_start(label, True, True, 0)

    check = Gtk.CheckButton()
    box.pack_start(check, True, True, 0)
    check.connect("toggled", callback)

    return box

class MatWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Simulação Ar Condicionado")
        self.Tac = 35  # The temperature of the coils
        self.Tout = 15  # The temperature of the outside air
        self.k = 0.03  # cooling coefficient(wall)
        self.kac = 0.1  # cooling coefficient(coils)
        self.Tc_low = 22  # control temperature(low)
        self.Tc_high = 24  # control temperature(high)

        self.Tr = 18  # initial room temperature
        self.tf = 100  # time extension for analysis
        self.n = 500  # step number
        self.mode = Mode.HEAT
        self.airConditioner = AirConditioner(self.Tr, self.Tac, self.Tout, self.k, self.kac, self.Tc_low, self.Tc_high, self.mode)
        self.integrators = [False] * Integrator.COUNT.value
        self.int_functions = [euler, taylor2, trapezium, mean, rk4, rkf, pc]
        self.int_res = [( [1], [1], 0, 0 )] * Integrator.COUNT.value

        self.set_border_width(10)
        self.set_default_size(1920, 1080)
        self.first_sim_run = False

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "Simulação Ar Condicionado"
        self.set_titlebar(header_bar)

        pane = Gtk.Paned()
        self.add(pane)

        frame1 = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        pane.pack1(frame1, True, True)

        param_frame = Gtk.Frame(label="Parametros Ar Condicionado")
        param_frame.set_shadow_type(Gtk.ShadowType.IN)
        frame1.add(param_frame)
        self.param_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        param_frame.add(self.param_box)


        box_tac = create_param_spin("Coils Temperature (Tac):", self.Tac, self.tac_spin_changed, 1.0)
        self.param_box.add(box_tac)
        box_tout = create_param_spin("Outside Air Temperature (Tout):", self.Tout, self.tout_spin_changed, 1.0)
        self.param_box.add(box_tout)
        box_k = create_param_spin("Wall cooling coefficient (k):", self.k, self.k_spin_changed, 0.01)
        self.param_box.add(box_k)
        box_kac = create_param_spin("Coils cooling coefficient (kac):", self.kac, self.kac_spin_changed, 0.01)
        self.param_box.add(box_kac)
        box_tc_low = create_param_spin("Low Control Temperature (Tc Low):", self.Tc_low, self.tc_low_spin_changed, 1.0)
        self.param_box.add(box_tc_low)
        box_tc_high = create_param_spin("High Control Temperature (Tc High):", self.Tc_high, self.tc_high_spin_changed, 1.0)
        self.param_box.add(box_tc_high)
        box_tr = create_param_spin("Initial Room Temperature (Tr):", self.Tr, self.tr_spin_changed, 1.0)
        self.param_box.add(box_tr)
        box_tf = create_param_spin("Time Extensionf for analysis (tf):", self.tf, self.tf_spin_changed, 1.0)
        self.param_box.add(box_tf)
        box_n = create_param_spin("Number of Steps (n):", self.n, self.n_spin_changed, 1.0)
        self.param_box.add(box_n)
        mode = Gtk.ListStore(int, str)
        mode.append([1, "Cool"])
        mode.append([2, "Heat"])
        name_combo = Gtk.ComboBox.new_with_model_and_entry(mode)
        name_combo.connect("changed", self.on_name_combo_changed)
        name_combo.set_entry_text_column(1)
        name_combo.set_active(1)
        self.param_box.add(name_combo)

        integrator_frame = Gtk.Frame(label="Método de Integração")
        integrator_frame.set_shadow_type(Gtk.ShadowType.IN)
        frame1.add(integrator_frame)
        self.int_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        integrator_frame.add(self.int_box)

        int_euler = create_integrator_type_checkbox("Euler: ", self.toggle_integrator_euler)
        int_taylor2 = create_integrator_type_checkbox("Taylor2: ", self.toggle_integrator_taylor2)
        int_trapezium = create_integrator_type_checkbox("Trapezium: ", self.toggle_integrator_trapezium)
        int_mean = create_integrator_type_checkbox("Mean: ", self.toggle_integrator_mean)
        int_rk4 = create_integrator_type_checkbox("RK4: ", self.toggle_integrator_rk4)
        int_rkf = create_integrator_type_checkbox("RKf: ", self.toggle_integrator_rkf)
        int_pc = create_integrator_type_checkbox("PC: ", self.toggle_integrator_pc)

        self.int_box.add(int_euler)
        self.int_box.add(int_taylor2)
        self.int_box.add(int_trapezium)
        self.int_box.add(int_mean)
        self.int_box.add(int_rk4)
        self.int_box.add(int_rkf)
        self.int_box.add(int_pc)

        sim_button = Gtk.Button.new_with_label("Simulate")
        sim_button.connect("clicked", self.simulate)
        self.int_box.pack_end(sim_button, False, True, 0)

        frame2 = Gtk.Frame()
        frame2.set_shadow_type(Gtk.ShadowType.IN)
        pane.pack2(frame2, True, True)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot()
        self.ax.grid(True)
        self.ax.set_title('Air conditioning a room')
        self.ax.set_xlabel('t')
        self.ax.set_ylabel('room temperature')
        self.canvas = FigureCanvas(self.fig)  # a Gtk.DrawingArea
        self.canvas.set_size_request(800, 600)
        frame2.add(self.canvas)

    def simulate(self, button):
        self.first_sim_run = True

        self.airConditioner = AirConditioner(self.Tr, self.Tac, self.Tout, self.k, self.kac, self.Tc_low, self.Tc_high, self.mode)
        self.airConditioner.reset_timer()

        t, Teuler = euler(self.airConditioner.act, 0, self.tf, self.n, self.Tr)
        self.int_res[Integrator.EULER.value] = (t, Teuler, self.airConditioner.get_period(), self.airConditioner.get_action_time())

        self.airConditioner.reset_timer()
        t, Ttaylor2 = taylor2(self.airConditioner.act, self.airConditioner.act_t, self.airConditioner.act_y, 0, self.tf, self.n, self.Tr)
        self.int_res[Integrator.TAYLOR2.value] = (t, Ttaylor2, self.airConditioner.get_period(), self.airConditioner.get_action_time())

        self.airConditioner.reset_timer()
        t, Ttrapezium = trapezium(self.airConditioner.act, 0, self.tf, self.n, self.Tr)
        self.int_res[Integrator.TRAPEZIUM.value] = (t, Ttrapezium, self.airConditioner.get_period(), self.airConditioner.get_action_time())

        self.airConditioner.reset_timer()
        t, Ttmean = mean(self.airConditioner.act, 0, self.tf, self.n, self.Tr)
        self.int_res[Integrator.MEAN.value] = (t, Ttmean, self.airConditioner.get_period(), self.airConditioner.get_action_time())

        self.airConditioner.reset_timer()
        t, Ttrk4 = rk4(self.airConditioner.act, 0, self.tf, self.n, self.Tr)
        self.int_res[Integrator.RK4.value] = (t, Ttrk4, self.airConditioner.get_period(), self.airConditioner.get_action_time())

        self.airConditioner.reset_timer()
        t, Ttrkf = rkf(self.airConditioner.act, 0, self.tf, self.Tr, 0.1, 0.1, 0.01)
        self.int_res[Integrator.RKF.value] = (t, Ttrkf, self.airConditioner.get_period(), self.airConditioner.get_action_time())

        self.airConditioner.reset_timer()
        t, Ttpc = pc(self.airConditioner.act, 0, self.tf, self.n, self.Tr)
        self.int_res[Integrator.PC.value] = (t, Ttpc, self.airConditioner.get_period(), self.airConditioner.get_action_time())

        self.plot(button)

    def plot(self, button):
        if (not self.first_sim_run):
            return

        self.ax.clear()
        self.ax.set_title('Air conditioning a room')
        self.ax.set_xlabel('t')
        self.ax.set_ylabel('room temperature')
        self.ax.grid(True)

        if (self.integrators[Integrator.EULER.value] == True):
            t = self.int_res[Integrator.EULER.value][0]
            Teuler = self.int_res[Integrator.EULER.value][1]
            period = self.int_res[Integrator.EULER.value][2]
            action_time = self.int_res[Integrator.EULER.value][3]
            self.ax.plot(t, Teuler, label="Euler, Period = " + str(period) + ", Action Time = " + str(action_time))

        if (self.integrators[Integrator.TAYLOR2.value] == True):
            t = self.int_res[Integrator.TAYLOR2.value][0]
            Ttaylor2 = self.int_res[Integrator.TAYLOR2.value][1]
            period = self.int_res[Integrator.TAYLOR2.value][2]
            action_time = self.int_res[Integrator.TAYLOR2.value][3]
            self.ax.plot(t, Ttaylor2, label="Taylor2, Period = " + str(period) + ", Action Time = " + str(action_time))

        if (self.integrators[Integrator.TRAPEZIUM.value] == True):
            t = self.int_res[Integrator.TRAPEZIUM.value][0]
            Ttrapezium = self.int_res[Integrator.TRAPEZIUM.value][1]
            period = self.int_res[Integrator.TRAPEZIUM.value][2]
            action_time = self.int_res[Integrator.TRAPEZIUM.value][3]
            self.ax.plot(t, Ttrapezium, label="Trapezium, Period = " + str(period) + ", Action Time = " + str(action_time))

        if (self.integrators[Integrator.MEAN.value] == True):
            t = self.int_res[Integrator.MEAN.value][0]
            Ttmean = self.int_res[Integrator.MEAN.value][1]
            period = self.int_res[Integrator.MEAN.value][2]
            action_time = self.int_res[Integrator.MEAN.value][3]
            self.ax.plot(t, Ttmean, label="Mean, Period = " + str(period) + ", Action Time = " + str(action_time))

        if (self.integrators[Integrator.RK4.value] == True):
            t = self.int_res[Integrator.RK4.value][0]
            Ttrk4 = self.int_res[Integrator.RK4.value][1]
            period = self.int_res[Integrator.RK4.value][2]
            action_time = self.int_res[Integrator.RK4.value][3]
            self.ax.plot(t, Ttrk4, label="RK4, Period = " + str(period) + ", Action Time = " + str(action_time))

        if (self.integrators[Integrator.RKF.value] == True):
            t = self.int_res[Integrator.RKF.value][0]
            Ttrkf = self.int_res[Integrator.RKF.value][1]
            period = self.int_res[Integrator.RKF.value][2]
            action_time = self.int_res[Integrator.RKF.value][3]
            self.ax.plot(t, Ttrkf, label="RKF, Period = " + str(period) + ", Action Time = " + str(action_time))

        if (self.integrators[Integrator.PC.value] == True):
            t = self.int_res[Integrator.PC.value][0]
            Ttpc = self.int_res[Integrator.PC.value][1]
            period = self.int_res[Integrator.PC.value][2]
            action_time = self.int_res[Integrator.PC.value][3]
            self.ax.plot(t, Ttpc, label="PC, Period = " + str(period) + ", Action Time = " + str(action_time))


        self.ax.legend()
        self.canvas.draw()

    def toggle_integrator_euler(self, integrator):
        self.integrators[Integrator.EULER.value] = not self.integrators[Integrator.EULER.value]
        self.plot(integrator)

    def toggle_integrator_taylor2(self, integrator):
        self.integrators[Integrator.TAYLOR2.value] = not self.integrators[Integrator.TAYLOR2.value]
        self.plot(integrator)

    def toggle_integrator_trapezium(self, integrator):
        self.integrators[Integrator.TRAPEZIUM.value] = not self.integrators[Integrator.TRAPEZIUM.value]
        self.plot(integrator)
        
    def toggle_integrator_mean(self, integrator):
        self.integrators[Integrator.MEAN.value] = not self.integrators[Integrator.MEAN.value]
        self.plot(integrator)

    def toggle_integrator_rk4(self, integrator):
        self.integrators[Integrator.RK4.value] = not self.integrators[Integrator.RK4.value]
        self.plot(integrator)

    def toggle_integrator_rkf(self, integrator):
        self.integrators[Integrator.RKF.value] = not self.integrators[Integrator.RKF.value]
        self.plot(integrator)

    def toggle_integrator_pc(self, integrator):
        self.integrators[Integrator.PC.value] = not self.integrators[Integrator.PC.value]
        self.plot(integrator)

    def tac_spin_changed(self, scroll):
        self.Tac = scroll.get_value()
    def tout_spin_changed(self, scroll):
        self.Tout = scroll.get_value()
    def k_spin_changed(self, scroll):
        self.k = scroll.get_value()
    def kac_spin_changed(self, scroll):
        self.kac = scroll.get_value()
    def tc_low_spin_changed(self, scroll):
        self.Tc_low = scroll.get_value()
    def tc_high_spin_changed(self, scroll):
        self.Tc_high = scroll.get_value()
    def tr_spin_changed(self, scroll):
        self.Tr = scroll.get_value()
    def tf_spin_changed(self, scroll):
        self.tf = scroll.get_value()
    def n_spin_changed(self, scroll):
        self.n = scroll.get_value()

    def on_name_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            if row_id == 1:
                self.mode = Mode.COOL
            else:
                self.mode = Mode.HEAT
