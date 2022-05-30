import napari_splineit2 as sit
import napari
from napari_splineit2.utils import phi_generator_impl
from napari_splineit2.splinegenerator import SplineCurveSample, B3, B2
import numpy as np
from skimage import data
import random
import types


from napari.layers.shapes import Shapes as ShapesLayer
from napari.layers.shapes.shapes import ShapeList as ShapeList
from napari.layers.shapes.shapes import Mode


from napari_splineit2.layer._shape_list import CtrlLayerShapeList
from napari_splineit2.layer._interpolated_layer import InterpolatedLayer
from napari_splineit2.layer.layer_factory import interpolation_factory





viewer = napari.view_image(data.camera(), name="photographer")
interpolation_factory(viewer)
napari.run()
