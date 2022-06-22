
import napari
from napari_splineit2.utils import phi_generator_impl,getCoefsFromKnots
from napari_splineit2.splinegenerator import SplineCurveSample, B3, B2
import numpy as np
from skimage import data
import random
import types

from napari.layers.shapes import Shapes as ShapesLayer
from napari.layers.shapes.shapes import ShapeList as ShapeList
from napari.layers.shapes.shapes import Mode
from ._shape_list import CtrlLayerShapeList



from napari._qt.layer_controls.qt_shapes_controls import QtShapesControls
from napari._qt.layer_controls.qt_layer_controls_container import layer_to_controls


class CtrlLayerControls(QtShapesControls):
    def __init__(self, *args, **kwargs):
        super(CtrlLayerControls, self).__init__(*args, **kwargs)

        # we only allow for polygon shapes and disable
        # all other shapes
        self.rectangle_button.setEnabled(False)
        self.ellipse_button.setEnabled(False)
        self.line_button.setEnabled(False)
        self.path_button.setEnabled(False)



def curve_from_cp(cp):

    if cp.shape[0]>3:
        cp = getCoefsFromKnots(cp, "cubic")    
        phi = phi_generator_impl(cp.shape[0], 20 * cp.shape[0], "cubic")
        SplineContour = SplineCurveSample(cp.shape[0], B3(), True, cp)
        curve = SplineContour.sample(phi)
        return curve
    return cp.copy()

class CtrlPtrLayer(ShapesLayer):
    def __init__(self, *args, interpolated_layer, **kwargs):
        self.interpolated_layer = interpolated_layer
        super(CtrlPtrLayer, self).__init__(*args,    
         edge_color="transparent",
        face_color="transparent",**kwargs)

        self._data_view = CtrlLayerShapeList(
            ndisplay=self._ndisplay,
            ctrl_layer=self,
            interpolated_layer=interpolated_layer,
        )
        self._data_view.slice_key = np.array(self._slice_indices)[
            list(self._dims_not_displayed)
        ]

    def add(self, data, *, shape_type, **kwargs):
        print(f"add {shape_type=}")
        if shape_type != "polygon" and shape_type!="path":
            raise RuntimeError("only polygon and path are supported")


        super(CtrlPtrLayer, self).add(data=data, shape_type=shape_type, **kwargs)

        interpolated = self.interpolate(data=data)
        self.interpolated_layer.add(data=data, shape_type=shape_type,**kwargs)

    def interpolate(self,data):
        return curve_from_cp(data)

    @property
    def shape_type(self):
        """list of str: name of shape type for each shape."""
        return self._data_view.shape_types

    @shape_type.setter
    def shape_type(self, shape_type):
        self._finish_drawing()

        new_data_view = CtrlLayerShapeList(
            ctrl_layer=self, interpolated_layer=interpolated_layer
        )
        shape_inputs = zip(
            self._data_view.data,
            ensure_iterable(shape_type),
            self._data_view.edge_widths,
            self._data_view.edge_color,
            self._data_view.face_color,
            self._data_view.z_indices,
        )

        self._add_shapes_to_view(shape_inputs, new_data_view)

        self._data_view = new_data_view
        self._update_dims()


layer_to_controls[CtrlPtrLayer] = CtrlLayerControls