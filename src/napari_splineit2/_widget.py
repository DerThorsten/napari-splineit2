"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/stable/npe2_manifest_specification.html

Replace code below according to your needs.
"""
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit
from magicgui import magic_factory

from .layer.layer_factory import interpolation_factory



class SplineitQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer


        self.layer_name_edit = QLineEdit("Splines")

        btn = QPushButton("Click me!!!!")
        btn.clicked.connect(self._on_click)



        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.layer_name_edit)
        self.layout().addWidget(btn)

    def _on_click(self):
        base_name = self.layer_name_edit.text()
        interpolation_factory(self.viewer, ctrl_layer_name=f"{base_name}-CTRL", interpolated_layer_name=f"{base_name}-Interpolated")


@magic_factory
def example_magic_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")


# Uses the `autogenerate: true` flag in the plugin manifest
# to indicate it should be wrapped as a magicgui to autogenerate
# a widget.
def example_function_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")
