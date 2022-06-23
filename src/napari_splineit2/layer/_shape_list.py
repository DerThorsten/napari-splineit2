import napari
import numpy as np
import types

from napari.layers.shapes import Shapes as ShapesLayer
from napari.layers.shapes.shapes import ShapeList as ShapeList
from napari.layers.shapes.shapes import Mode


class CtrlLayerShapeList(ShapeList):
    def __init__(self, *args, ctrl_layer, interpolated_layer, **kwargs):
        self.ctrl_layer = ctrl_layer
        self.interpolated_layer = interpolated_layer
        super(CtrlLayerShapeList, self).__init__(*args, **kwargs)
        self.mode = "DIRECT"

    def edit(self, index, data, face_color=None, edge_color=None, new_type=None):
        print(f"edit {index=}")

        if self.ctrl_layer._mode == Mode.VERTEX_INSERT:

            print("insert value:", self.ctrl_layer._moving_value)
        else:
            print("moving value:", self.ctrl_layer._moving_value)
        super(CtrlLayerShapeList, self).edit(
            index=index,
            data=data,
            face_color=face_color,
            edge_color=edge_color,
            new_type=new_type,
        )

        new_data = self.ctrl_layer.interpolate(data)

        self.update_interpolated(index=index, data=new_data, new_type=new_type)


    def run_interpolation(self):
        for index,s in enumerate(self.shapes):
            new_data = self.ctrl_layer.interpolate(s.data)
            self.update_interpolated(index=index, data=new_data, new_type=None)
        self.interpolated_layer.refresh()

    def update_interpolated(self, data, index, new_type=None):
        with self.interpolated_layer.events.set_data.blocker():
            self.interpolated_layer._data_view.edit(index=index, data=data, new_type=new_type)
            self.interpolated_layer._data_view._update_displayed()
        self.interpolated_layer.refresh()


    def shift(self, index, shift):
        print(f"shift {index=} {shift=}")
        self.interpolated_layer._data_view.shift(index, shift.copy())
        super(CtrlLayerShapeList, self).shift(index, shift.copy())
        self.interpolated_layer.refresh()

    def scale(self, index, scale, center=None):
        print(f"scale {index=} {scale=}    {type(index)=}  {type(center)=}")
        self.interpolated_layer._data_view.scale(index, scale, center)
        super(CtrlLayerShapeList, self).scale(index, scale, center)
        self.interpolated_layer.refresh()

    def rotate(self, index, angle, center=None):
        print(f"rotate {index=} {angle=}")
        self.interpolated_layer._data_view.rotate(index, angle, center)
        super(CtrlLayerShapeList, self).rotate(index, angle, center)
        self.interpolated_layer.refresh()

    def flip(self, index, axis, center=None):
        print(f"flip {index=} {axis=}")
        self.interpolated_layer._data_view.flip(index, axis, center)
        super(CtrlLayerShapeList, self).flip(index, axis, center)
        self.interpolated_layer.refresh()

    def transform(self, index, transform):
        print(f"transform {index=} {transform=}")
        self.interpolated_layer._data_view.transform(index, transform.copy())
        super(CtrlLayerShapeList, self).transform(index, transform.copy())
        self.interpolated_layer.refresh()


    # def add(self,*args, **kwargs):
    #     print(f"add")
    #     self.interpolated_layer._data_view.add(index, transform.copy())
    #     super(CtrlLayerShapeList, self).transform(index, transform.copy())
    #     self.interpolated_layer.refresh()

    def update_z_index(self, index, z_index):
        print(f"update_z_index {index=} {z_index=}")
        self.interpolated_layer._data_view.update_z_index(index, z_index)
        super(CtrlLayerShapeList, self).update_z_index(index, z_index)
        self.interpolated_layer.refresh()

    def remove(self, index, renumber=True):
        print(f"remove {index=} {renumber=}")
        if renumber:
            self.interpolated_layer._data_view.remove(index, renumber)
        super(CtrlLayerShapeList, self).remove(index, renumber)
        if renumber:
            self.interpolated_layer.refresh()

