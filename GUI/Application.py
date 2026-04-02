from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt

from GUI.Views.SVGCanvasView import SVGCanvasView
from GUI.Widgets.SpacingControl import SpacingControl
from GUI.Widgets.ScaleControl import ScaleControl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Handwriting Synthesis - GUI")
        self.resize(1280, 720)

        root = QWidget()
        self.setCentralWidget(root)

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        #canvas
        self.canvas = SVGCanvasView()
        root_layout.addWidget(self.canvas, stretch=1)

        #sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setContentsMargins(12, 12, 12, 12)
        sidebar_layout.setSpacing(12)
        root_layout.addWidget(sidebar)

        #controls
        self.spacing_control = SpacingControl(default=60)
        self.spacing_control.valueChanged.connect(self.canvas.set_line_spacing)
        sidebar_layout.addWidget(self.spacing_control)

        self.scale_control = ScaleControl(default=1.0)
        self.scale_control.valueChanged.connect(self.canvas.set_handwriting_scale)
        sidebar_layout.addWidget(self.scale_control)