from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget
from PySide6.QtCore import Qt

from GUI.Views.SVGCanvasView import SVGCanvasView
from GUI.Widgets.NotebookPaperControls import NotebookPaperControls
from GUI.Widgets.HandwritingControls import HandwritingControls
from GUI.Widgets.HandwritingInput import HandwritingInput

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

        #Text tab
        self.handwriting_input = HandwritingInput()
        self.handwriting_input.valueChanged.connect(self.canvas.generate_handwriting)
        tabs.addTab(self.handwriting_input, "Text")
        
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