import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from air_conditioner import AirConditioner, Mode
from methods import euler, taylor2, trapezium, mean, rk4, rkf, pc

def create_param_spin(title, initial, callback):
    adjustment = Gtk.Adjustment(upper=500, step_increment=0.1, page_increment=1)
    box_param = Gtk.Box()
    box_param.set_homogeneous(False)

    param_label = Gtk.Label(label=title)
    box_param.pack_start(param_label, True, True, 0)
    param_spin_button = Gtk.SpinButton()
    param_spin_button.set_adjustment(adjustment)
    param_spin_button.set_numeric(True)
    param_spin_button.set_digits(5)
    param_spin_button.set_value(initial)
    param_spin_button.connect("value-changed", callback)
    box_param.pack_start(param_spin_button, True, True, 0)

    return box_param


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

        self.set_border_width(10)
        self.set_default_size(1920, 1080)

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "Simulação Ar Condicionado"
        self.set_titlebar(header_bar)

        pane = Gtk.Paned()
        self.add(pane)

        frame1 = Gtk.Frame()
        frame1.set_shadow_type(Gtk.ShadowType.IN)
        pane.pack1(frame1, True, True)

        param_frame = Gtk.Frame(label="Parametros Ar Condicionado")
        param_frame.set_shadow_type(Gtk.ShadowType.IN)
        frame1.add(param_frame)
        self.param_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        param_frame.add(self.param_box)


        box_tac = create_param_spin("Tac:", self.Tac, self.tac_spin_changed)
        self.param_box.add(box_tac)
        box_tout = create_param_spin("Tout:", self.Tout, self.tout_spin_changed)
        self.param_box.add(box_tout)
        box_k = create_param_spin("k:", self.k, self.k_spin_changed)
        self.param_box.add(box_k)
        box_kac = create_param_spin("kac:", self.kac, self.kac_spin_changed)
        self.param_box.add(box_kac)
        box_tc_low = create_param_spin("Tc low:", self.Tc_low, self.tc_low_spin_changed)
        self.param_box.add(box_tc_low)
        box_tc_high = create_param_spin("Tc high:", self.Tc_high, self.tc_high_spin_changed)
        self.param_box.add(box_tc_high)
        box_tr = create_param_spin("Tr:", self.Tr, self.tr_spin_changed)
        self.param_box.add(box_tr)
        box_tf = create_param_spin("Tf:", self.tf, self.tf_spin_changed)
        self.param_box.add(box_tf)
        box_n = create_param_spin("Steps:", self.n, self.n_spin_changed)
        self.param_box.add(box_n)

        # Just for testing
        temp_button = Gtk.Button.new_with_label("Simulate")
        temp_button.connect("clicked", self.plot)
        self.param_box.add(temp_button)
        #####

        frame2 = Gtk.Frame()
        frame2.set_shadow_type(Gtk.ShadowType.IN)
        pane.pack2(frame2, True, True)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot()
        self.canvas = FigureCanvas(self.fig)  # a Gtk.DrawingArea
        self.canvas.set_size_request(800, 600)
        frame2.add(self.canvas)

    def plot(self, button):
        self.airConditioner = AirConditioner(self.Tr, self.Tac, self.Tout, self.k, self.kac, self.Tc_low, self.Tc_high, self.mode)
        t, Teuler = euler(self.airConditioner.act, 0, self.tf, self.n, self.Tr)
        self.ax.clear()
        self.ax.plot(t, Teuler)
        self.canvas.draw()

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
