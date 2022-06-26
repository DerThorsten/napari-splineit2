"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/plugins/stable/npe2_manifest_specification.html

Replace code below according to your needs.
"""
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit
from magicgui import magic_factory

from .layer.layer_factory import layer_factory
from .interpolation import CubicInterpolator,SplineInterpolator


class SplineitQWidget(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        # add the widgets
        self._setup_ui()

        # connect the widgets events / signals
        self._connect_ui()


    def _setup_ui(self):
        self._layer_name_edit = QLineEdit("Splines")
        self._add_layer_btn = QPushButton("Click me!!!!")
        

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self._layer_name_edit)
        self.layout().addWidget(self._add_layer_btn)

    def _connect_ui(self):
        self._add_layer_btn.clicked.connect(self._on_click)

    # todo check for name clashes
    def _get_layer_base_name(self):
        base_name = self._layer_name_edit.text()
        return base_name



    def _on_click(self):
        interpolator = CubicInterpolator()
        interpolator = SplineInterpolator(k=3)
        base_name = self._get_layer_base_name()
        layer_factory(self.viewer, 
            interpolator=interpolator, 
            ctrl_layer_name=f"{base_name}-CTRL", 
            interpolated_layer_name=f"{base_name}-Interpolated")