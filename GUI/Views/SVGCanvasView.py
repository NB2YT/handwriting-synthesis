from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPainter

from GUI.Workers.HandwritingWorker import HandwritingWorker
from SVG.AbsoluteVectorGraphic import AbsoluteVectorGraphic
from SVG.Handwriting import Handwriting

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

        self._svg_items = []
        self._handwriting_line_spacing = 60
        self._handwriting_scale = 1.0
        self._current_avg: AbsoluteVectorGraphic = None
        self._current_handwriting: Handwriting = None
        self._is_first_load = True
        
        self._worker = HandwritingWorker()
        self._worker.finished.connect(self.apply_svg)
        self._worker.start()
        self.destroyed.connect(self._worker.terminate)

    @Slot(AbsoluteVectorGraphic, Handwriting)
    def apply_svg(self, avg: AbsoluteVectorGraphic, handwriting: Handwriting):
        self._current_avg = avg
        self._current_handwriting = handwriting
        self._current_handwriting.set_spacing(self._handwriting_line_spacing)
        self._current_handwriting.set_scale(self._handwriting_scale)
        self._redraw()

        #center when loaded
        if self._is_first_load:
            self.center_on_svg_items()
            self._is_first_load = False

    @Slot(int)
    def set_line_spacing(self, value: int):
        self._handwriting_line_spacing = value
        if self._current_avg:
            self._current_handwriting.set_spacing(value)
            self._redraw()

    @Slot(float)
    def set_handwriting_scale(self, value: float):
        self._handwriting_scale = value
        if self._current_avg:
            self._current_handwriting.set_scale(value)
            self._redraw()

    def _redraw(self):
        for item in self._svg_items:
            self._scene.removeItem(item)
        self._svg_items.clear()

        for item in self._current_avg.as_graphics_items():
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