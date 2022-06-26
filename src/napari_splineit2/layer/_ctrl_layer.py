
import napari

import numpy as np
from skimage import data
import random
import types

from qtpy.QtWidgets import QComboBox

from ..interpolation import registered_interplators,interpolator_factory
from ._shape_list import CtrlLayerShapeList

import napari.layers
from napari.layers.shapes import Shapes as ShapesLayer
from napari.layers.shapes.shapes import ShapeList as ShapeList
from napari.layers.shapes.shapes import Mode
from napari._qt.layer_controls.qt_shapes_controls import QtShapesControls
from napari._qt.layer_controls.qt_layer_controls_container import layer_to_controls



class CtrlLayerControls(QtShapesControls):
    def __init__(self, layer):
        super(CtrlLayerControls, self).__init__(layer)

        # we only allow for polygon shapes and disable all other shapes
        self.rectangle_button.setEnabled(False)
        self.ellipse_button.setEnabled(False)
        self.line_button.setEnabled(False)
        self.path_button.setEnabled(False)



        # the current interpolator
        interpolator_type = type(layer.interpolator)

        # # dropdown list with all interpolator types
        self.method_selector = QComboBox()
        self.method_selector.addItems(registered_interplators.keys())
        self.method_selector.setCurrentText(interpolator_type.name)
        self.method_selector.currentIndexChanged.connect(self.on_method_change)

        # the ui of the interpolator itself
        self.layer_ui = interpolator_type.UI(layer=layer)

        self.layout().addRow("method", self.method_selector)
        self.layout().addRow(self.layer_ui)


        # keep track of the parameters of the individual method
        # st. we can restore the last used parameter when 
        # a already used method is selected from the combo box
        self.method_kwargs = {
            interpolator_type.name : layer.interpolator.marshal()
        }

    def on_method_change(self):

        # store the parameters of the last method
        last_method = self.layer.interpolator
        self.method_kwargs[type(last_method).name] = last_method.marshal()

        # the new method
        new_method_name = self.method_selector.currentText()

        # restore parameters
        kwargs = self.method_kwargs.get(new_method_name, {})
        interpolator = interpolator_factory(name=new_method_name, **kwargs)
        self.layer.interpolator = interpolator

        # remove old control ui and add new ui
        interpolator_ui_cls = type(interpolator).UI
        self.layout().removeRow(self.layer_ui)
        self.layer_ui = interpolator_ui_cls(layer=self.layer)
        self.layout().addRow(self.layer_ui)

        # run interpolation 
        self.layer.run_interpolation()


class CtrlPtrLayer(ShapesLayer):
    def __init__(self, *args, interpolator, interpolated_layer, **kwargs):
        self.interpolator = interpolator
        self.interpolated_layer = interpolated_layer
        self.interpolated_layer.ctrl_layer = self
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

    # needed to make writer possible
    @property
    def _type_string(self):
        return "shapes"

    def add(self, data, *, shape_type, **kwargs):
        if shape_type != "polygon" and shape_type!="path":
            raise RuntimeError("only polygon and path are supported")

        if isinstance(data, list):

            interpolated_polygons = [self.interpolate(data=poly) for poly in data]
            super(CtrlPtrLayer, self).add(data=data, shape_type=shape_type, **kwargs)
            self.interpolated_layer.add(data=interpolated_polygons, shape_type=shape_type,**kwargs)

        else:

            super(CtrlPtrLayer, self).add(data=data, shape_type=shape_type, **kwargs)
            interpolated = self.interpolate(data=data)
            self.interpolated_layer.add(data=interpolated, shape_type=shape_type,**kwargs)

    def interpolate(self,data):
        return self.interpolator(data)

    def run_interpolation(self):
        self._data_view.run_interpolation()

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


# to be able to use this custom layer with reader/writer plugins
# we need to add the layer into the `napari.layer` module
# TODO explain the renaming
napari.layers.Splineit_Ctrl = CtrlPtrLayer
napari.layers.NAMES.add("splineit_ctrl")
