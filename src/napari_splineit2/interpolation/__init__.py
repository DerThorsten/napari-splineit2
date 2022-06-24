import numpy as np

from scipy.interpolate import CubicSpline,splrep,splev

from ..utils import phi_generator_impl,getCoefsFromKnots
from ..splinegenerator import SplineCurveSample, B3, B2


from qtpy.QtWidgets import QWidget,QHBoxLayout,QSlider,QFormLayout,QDoubleSpinBox,QSpinBox
from qtpy.QtCore import Qt,QSignalBlocker,Signal

def curve_from_cp(cp):

    if cp.shape[0]>3:
        cp = getCoefsFromKnots(cp, "cubic")    
        phi = phi_generator_impl(cp.shape[0], 20 * cp.shape[0], "cubic")
        SplineContour = SplineCurveSample(cp.shape[0], B3(), True, cp)
        curve = SplineContour.sample(phi)
        return curve
    return cp.copy()


class SpinSlider(QWidget):

    valueChanged = Signal(int)

    def __init__(self, minmax, value):
        super(SpinSlider, self).__init__()




        layout = QHBoxLayout()
        self.setLayout(layout)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setTickInterval(1)
        self.slider.setMinimum(minmax[0])
        self.slider.setMaximum(minmax[1])
        self.slider.setValue(value)
        self.slider.valueChanged.connect(self._on_slider_changed)

        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(minmax[0])
        self.spinbox.setMaximum(minmax[1])
        self.spinbox.setValue(value)
        self.spinbox.valueChanged.connect(self._on_spin_box_canged)

        layout.addWidget(self.spinbox,1)
        layout.addWidget(self.slider,4)

    def value(self):
        return self.slider.value()

    def _on_slider_changed(self):

        with QSignalBlocker(self.spinbox) as blocker:
            self.spinbox.setValue(self.slider.value())

        self.valueChanged.emit(self.slider.value())

    def _on_spin_box_canged(self):
        with QSignalBlocker(self.slider) as blocker:
            self.slider.setValue(self.spinbox.value())
        self.valueChanged.emit(self.slider.value())


class SplineInterpolatorUI(QWidget):
    def __init__(self, layer):
        super(SplineInterpolatorUI, self).__init__()
        self.layer = layer
        self.interpolator = self.layer.interpolator
        layout = QFormLayout()
        self.setLayout(layout)

        # self.order_slider = QSlider(Qt.Horizontal)
        # self.order_slider.setTickInterval(1)
        # self.order_slider.setMinimum(1)
        # self.order_slider.setMaximum(3)
        # self.order_slider.setValue(self.interpolator.k)
        # self.order_slider.valueChanged.connect(self.on_order_changed)

        self.order_widget = SpinSlider(minmax=[1,3], value=self.interpolator.k)
        self.order_widget.valueChanged.connect(self.on_order_changed)

        self.s_widget = SpinSlider(minmax=[0,50000], value=int(self.interpolator.s))
        self.s_widget.valueChanged.connect(self.on_s_changed)

        self.n_widget = SpinSlider(minmax=[1,100], value=int(self.interpolator.n))
        self.n_widget.valueChanged.connect(self.on_n_changed)


        layout.addRow("k",self.order_widget)
        layout.addRow("s",self.s_widget)
        layout.addRow("n",self.n_widget)

    def on_n_changed(self):
        value = self.n_widget.value()
        self.interpolator.n = value
        self.layer.run_interpolation()

    def on_s_changed(self):
        value = self.s_widget.value()
        self.interpolator.s = value
        self.layer.run_interpolation()

    def on_order_changed(self):
        value = self.order_widget.value()
        # print("on_order_changed",value)
        self.interpolator.k = int(value)
        self.layer.run_interpolation()

class SplineInterpolator(object):
    
    UI = SplineInterpolatorUI
    name = "SplineInterpolator"

    def __init__(self, k=3, s=0.0, n=10):
        self.k = k
        self.s = s
        self.n = n

    def __call__(self, ctrl_points):
        ctrl_points = np.require(ctrl_points)
        if ctrl_points.shape[0] < 3:
     
            first_point = ctrl_points[0,:]
            return np.concatenate([ctrl_points, first_point[None,:]], axis=0)
          
        else:

            first_point = ctrl_points[0,:]
            ctrl_points =  np.concatenate([ctrl_points, first_point[None,:]], axis=0)

            t = np.arange(ctrl_points.shape[0])

            cs_x = splrep(t, ctrl_points[:,0], per=True,k=self.k, s=self.s)
            cs_y = splrep(t, ctrl_points[:,1], per=True,k=self.k, s=self.s)
            tfine = np.linspace(0, t[-1], self.n * ctrl_points.shape[0])
            xx = splev(tfine, cs_x)[:,None]
            yy = splev(tfine, cs_y)[:,None]

            print(xx.shape,yy.shape)

            ret =  np.concatenate([xx, yy], axis=1)
            print(ret.shape)
            return ret

    # return a dict which can be passed to constructor
    def marshal(self):
        return {
            "k":self.k,
            "s":self.s,
            "n":self.n
        }

class CubicInterpolatorUI(QWidget):
    def __init__(self, layer):
        super(CubicInterpolatorUI, self).__init__()
        self.layer = layer

class CubicInterpolator(object):
    
    UI = CubicInterpolatorUI
    name = "CubicInterpolator"


    def __call__(self, ctrl_points):
        ctrl_points = np.require(ctrl_points)
        if ctrl_points.shape[0] < 3:
            first_point = ctrl_points[0,:]
            return np.concatenate([ctrl_points, first_point[None,:]], axis=0)

        else:

            first_point = ctrl_points[0,:]
            ctrl_points =  np.concatenate([ctrl_points, first_point[None,:]], axis=0)

            t = np.arange(ctrl_points.shape[0])
            cs_x = CubicSpline(t, ctrl_points[:,0], bc_type='periodic')
            cs_y = CubicSpline(t, ctrl_points[:,1], bc_type='periodic')
            tfine = np.linspace(0, t[-1])
            xx = cs_x(tfine)[:,None]
            yy = cs_y(tfine)[:,None]

    
            ret =  np.concatenate([xx, yy], axis=1)
            return ret

    def marshal(self):
        return dict()


interpolators = {
    CubicInterpolator.name : CubicInterpolator,
    SplineInterpolator.name : SplineInterpolator
}


def interpolator_factory(name, **kwargs):
    return interpolators[name](**kwargs)