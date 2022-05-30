from napari.layers.shapes import Shapes as ShapesLayer
from napari.layers.shapes.shapes import Mode

class InterpolatedLayer(ShapesLayer):
    def __init__(self, *args, **kwargs):
        super(InterpolatedLayer, self).__init__(*args,**kwargs)
        self.mode = Mode.PAN_ZOOM
