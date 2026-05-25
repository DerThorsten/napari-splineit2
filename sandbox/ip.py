import napari
from skimage import data


from napari_splineit2.layer.layer_factory import interpolation_factory

viewer = napari.view_image(data.coins(), name="coins")
interpolation_factory(viewer)
napari.run()
