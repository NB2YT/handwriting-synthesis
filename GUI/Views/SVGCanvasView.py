from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtSvgWidgets import QGraphicsSvgItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter

from GUI.Workers.HandwritingWorker import HandwritingWorker
from SVG.AbsoluteVectorGraphic import AbsoluteVectorGraphic

class SVGCanvasView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        #allow panning
        self.scene.setSceneRect(-5000, -5000, 10000, 10000)
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

        self.svg_items = []
        self.is_first_load = True
        
        self.worker = HandwritingWorker()
        self.worker.finished.connect(self.apply_svg)
        self.worker.start()
        self.destroyed.connect(self.worker.terminate)

    def apply_svg(self, avg: AbsoluteVectorGraphic):
        for item in self.svg_items:
            self.scene.removeItem(item)
        self.svg_items.clear()

        for item in avg.as_graphics_items():
            self.scene.addItem(item)
            self.svg_items.append(item)

        #center when loaded
        if self.is_first_load:
            self.center_on_svg_items()
            self.is_first_load = False

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
        if not self.svg_items:
            return

        # Unite all item bounding rects into one
        combined = self.svg_items[0].sceneBoundingRect()
        for item in self.svg_items[1:]:
            combined = combined.united(item.sceneBoundingRect())
        
        self.centerOn(combined.center())