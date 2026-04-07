from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget
from PySide6.QtCore import Qt

from GUI.Views.SVGCanvasView import SVGCanvasView
from GUI.Widgets.SpacingControl import SpacingControl
from GUI.Widgets.ScaleControl import ScaleControl

from GUI.Widgets.NotebookPaperControls import NotebookPaperControls
from GUI.Widgets.HandwritingControls import HandwritingControls

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
        tabs = QTabWidget()
        tabs.setFixedWidth(220)
        root_layout.addWidget(tabs)

        '''
        #handwriting tab
        handwriting_tab = QWidget()
        handwriting_layout = QVBoxLayout(handwriting_tab)
        handwriting_layout.setAlignment(Qt.AlignTop)
        handwriting_layout.setContentsMargins(12, 12, 12, 12)
        handwriting_layout.setSpacing(12)

        #handwriting controls
        self.spacing_control = SpacingControl(default=60)
        self.spacing_control.valueChanged.connect(self.canvas.set_line_spacing)
        handwriting_layout.addWidget(self.spacing_control)

        self.scale_control = ScaleControl(default=1.0)
        self.scale_control.valueChanged.connect(self.canvas.set_handwriting_scale)
        handwriting_layout.addWidget(self.scale_control)

        tabs.addTab(handwriting_tab, "Handwriting")
        '''

        #handwriting tab
        self.handwriting_controls = HandwritingControls()
        self.handwriting_controls.valueChanged.connect(self.canvas.set_handwriting_config)
        self.canvas.set_handwriting_config(self.handwriting_controls.value())
        tabs.addTab(self.handwriting_controls, "Handwriting")

        #paper tab
        self.paper_controls = NotebookPaperControls()
        self.paper_controls.valueChanged.connect(self.canvas.set_notebook_paper)
        self.canvas.set_notebook_paper(self.paper_controls.value())
        tabs.addTab(self.paper_controls, "Paper")