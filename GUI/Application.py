from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QFileDialog
from PySide6.QtCore import Qt

from GUI.Views.SVGCanvasView import SVGCanvasView
from GUI.Widgets.NotebookPaperControls import NotebookPaperControls
from GUI.Widgets.HandwritingControls import HandwritingControls
from GUI.Widgets.HandwritingInput import HandwritingInput
from GUI.Workers.HandwritingWorker import HandwritingWorker

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

        #handwriting worker setup
        self.handwriting_worker = HandwritingWorker()
        self.handwriting_worker.start()

        #canvas
        self.canvas = SVGCanvasView()
        root_layout.addWidget(self.canvas, stretch=1)
        self.handwriting_worker.finished.connect(self.canvas.apply_handwriting)

        #sidebar
        tabs = QTabWidget()
        tabs.setFixedWidth(220)
        root_layout.addWidget(tabs)

        #Text tab
        self.handwriting_input = HandwritingInput()
        self.handwriting_input.valueChanged.connect(self.handwriting_worker.generate)
        self.handwriting_worker.processing.connect(self.handwriting_input.set_processing)
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

        #export svg
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        export_action = file_menu.addAction("Export SVG")
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self._on_export)

    #TODO: make this better
    def _on_export(self):
        if self.canvas._current_notebook_paper is None:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export SVG", "", "SVG Files (*.svg)")
        if path:
            if not path.endswith(".svg"):
                path += ".svg"
            svg = self.canvas._avg.as_drawing(
                size=(
                        self.canvas._current_notebook_paper.width,
                        self.canvas._current_notebook_paper.height,
                    )
            ).as_svg()
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
    
    def closeEvent(self, event):
        self.handwriting_worker.stop()
        super().closeEvent(event)