from napari.utils.events import Event

from . _shape_list import CtrlLayerShapeList
from . _interpolated_layer import InterpolatedLayer
from . _ctrl_layer import CtrlPtrLayer


def interpolation_factory(viewer, ctrl_layer_name="CtrLayer", interpolated_layer_name="Interpolated"):


    interpolated_layer = InterpolatedLayer(name=interpolated_layer_name)
    viewer.add_layer(interpolated_layer)

    ctrl_layer = CtrlPtrLayer(name=ctrl_layer_name, interpolated_layer=interpolated_layer)
    viewer.add_layer(ctrl_layer)


    # if either of the layers is deleted
    # we also delete the other one
    def on_removed(event: Event):
        layer = event.value
        if layer == interpolated_layer:
            if ctrl_layer in viewer.layers:
                viewer.layers.remove(ctrl_layer)
        elif layer == ctrl_layer:
            if interpolated_layer in viewer.layers:
                viewer.layers.remove(interpolated_layer)
    viewer.layers.events.removed.connect(on_removed)





    return interpolated_layer, ctrl_layer