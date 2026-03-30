from PySide6.QtWidgets import QMainWindow

from GUI.Views.SVGCanvasView import SVGCanvasView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Handwriting Synthesis - GUI")
        self.resize(1280, 720)
        
        self.viewer = SVGCanvasView()
        self.setCentralWidget(self.viewer)