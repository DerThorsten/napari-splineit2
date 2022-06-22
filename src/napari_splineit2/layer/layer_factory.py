from . _shape_list import CtrlLayerShapeList
from . _interpolated_layer import InterpolatedLayer
from . _ctrl_layer import CtrlPtrLayer

def interpolation_factory(viewer, ctrl_layer_name="CtrLayer", interpolated_layer_name="Interpolated"):

    interpolated_layer = InterpolatedLayer(name=interpolated_layer_name)
    viewer.add_layer(interpolated_layer)

    ctrl_layer = CtrlPtrLayer(name=ctrl_layer_name, interpolated_layer=interpolated_layer)
    viewer.add_layer(ctrl_layer)

    return interpolated_layer, ctrl_layer