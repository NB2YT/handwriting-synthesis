from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPainter

from GUI.Workers.HandwritingWorker import HandwritingWorker
from SVG.AbsoluteVectorGraphic import AbsoluteVectorGraphic
from SVG.Handwriting import Handwriting, HandwritingTransformConfig, HandwritingGenerationConfig
from SVG.NotebookPaperGenerator import NotebookPaper

class SVGCanvasView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        #allow panning
        self._scene.setSceneRect(-5000, -5000, 10000, 10000)
        self.centerOn(0, 0)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Enable dragging/panning with the left mouse button
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        # Smooth out the rendering
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)

        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)

        self._avg = AbsoluteVectorGraphic()
        self._svg_items = []
        self._handwriting_line_spacing = 60
        self._handwriting_scale = 1.0
        self._current_notebook_paper: NotebookPaper = None
        self._current_handwriting: Handwriting = None
        self._handwriting_config: HandwritingTransformConfig = None
        self._is_first_load = True
        
        self._worker = HandwritingWorker()
        self._worker.finished.connect(self.apply_handwriting)
        self._worker.start()
        self.destroyed.connect(self._worker.terminate)

    @Slot(Handwriting)
    def apply_handwriting(self, handwriting: Handwriting):
        self._current_handwriting = handwriting
        handwriting.apply_config(self._handwriting_config)
        self._redraw()

        #center when loaded
        if self._is_first_load:
            self.center_on_svg_items()
            self._is_first_load = False

    @Slot(HandwritingGenerationConfig)
    def generate_handwriting(self, config: HandwritingGenerationConfig):
        self._worker.generate(config)

    @Slot(NotebookPaper)
    def set_notebook_paper(self, notebook_paper: NotebookPaper):
        self._current_notebook_paper = notebook_paper
        self._redraw()

    @Slot(HandwritingTransformConfig)
    def set_handwriting_config(self, config: HandwritingTransformConfig):
        self._handwriting_config = config
        if self._current_handwriting:
            self._current_handwriting.apply_config(config)
        self._redraw()

    def _redraw(self):
        self._avg = AbsoluteVectorGraphic()
        if self._current_notebook_paper:
            self._avg.append(self._current_notebook_paper)
        if self._current_handwriting:
            self._avg.append(self._current_handwriting)

        for item in self._svg_items:
            self._scene.removeItem(item)
        self._svg_items.clear()

        for item in self._avg.as_graphics_items():
            self._scene.addItem(item)
            self._svg_items.append(item)

    def wheelEvent(self, event):
        # Zoom Factor
        zoom_in = 1.25
        zoom_out = 1 / zoom_in

        # Check wheel direction
        if event.angleDelta().y() > 0:
            self.scale(zoom_in, zoom_in)
        else:
            self.scale(zoom_out, zoom_out)
    
    def center_on_svg_items(self):
        self.centerOn(self._scene.itemsBoundingRect().center())