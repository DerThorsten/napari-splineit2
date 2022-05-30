from . _shape_list import CtrlLayerShapeList
from . _interpolated_layer import InterpolatedLayer
from . _ctrl_layer import CtrlPtrLayer

def interpolation_factory(viewer):

    interpolated_layer = InterpolatedLayer(name="Interpolated")
    viewer.add_layer(interpolated_layer)

    ctrl_layer = CtrlPtrLayer(name="CtrLayer", interpolated_layer=interpolated_layer)
    viewer.add_layer(ctrl_layer)

    return interpolated_layer, ctrl_layer