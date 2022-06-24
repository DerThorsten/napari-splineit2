import json
import numpy

from . interpolation import interpolator_factory
from .layer.layer_factory import layer_factory
from napari.components.viewer_model import ViewerModel


def get_reader(path):
    # If we recognize the format, we return the actual reader function
    if isinstance(path, str) and path.endswith(".splineit"):
        return splineit_file_reader
    # otherwise we return None.
    return None


def splineit_file_reader(path):
    
    with open(path, 'r') as f:
        raw_data = json.load(f)        

    # the data
    list_of_polygons = raw_data['data']
    list_of_polygons = [numpy.array(p) for p in list_of_polygons]

    for poly in list_of_polygons:
        print("PS",poly.shape, poly.dtype)

    # the interpolator arguments
    name = raw_data['method']['name']
    kwargs = raw_data['method']['args']
    interpolator = interpolator_factory(name=name, **kwargs)

    layer_attributes = {"interpolator": interpolator}
    return [(list_of_polygons, layer_attributes, "splineit_ctrl")]


# TODO document
def add_splineit_ctrl(self,data, name, interpolator):
    interpolated_layer, ctrl_layer = layer_factory(viewer=self, data=data, interpolator=interpolator,
        ctrl_layer_name=f"{name}",
        interpolated_layer_name=f"{name}-IP"
    )
    return interpolated_layer, ctrl_layer

ViewerModel.add_splineit_ctrl = add_splineit_ctrl