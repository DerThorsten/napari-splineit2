import napari
from skimage import data

from napari.layers.shapes import Shapes as ShapesLayer
from napari.layers.shapes.shapes import ShapeList as ShapeList
from napari.layers.shapes.shapes import Mode

from napari_splineit2.layer._shape_list import CtrlLayerShapeList
from napari_splineit2.layer._interpolated_layer import InterpolatedLayer
from napari_splineit2.layer.layer_factory import interpolation_factory

viewer = napari.view_image(data.coins(), name="coins")
interpolation_factory(viewer)
napari.run()
