from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPainter, QKeyEvent, QMouseEvent, QScrollEvent

from SVG.AbsoluteVectorGraphic import AbsoluteVectorGraphic
from SVG.Handwriting import Handwriting, HandwritingTransformConfig
from SVG.NotebookPaperGenerator import NotebookPaper
from SVG.Transform.TransformHandles import TransformHandles
from SVG.Transform.HandwritingGroup import HandwritingGroup

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

        #default to select mode — pan is middle mouse or space+drag
        self.setDragMode(QGraphicsView.RubberBandDrag)
        #Smooth out the rendering
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
        self._handles: TransformHandles = None
        self._space_held = False

        self._scene.selectionChanged.connect(self._on_selection_changed)

    @Slot(Handwriting)
    def apply_handwriting(self, handwriting: Handwriting):
        self._current_handwriting = handwriting
        handwriting.apply_config(self._handwriting_config)
        self._redraw()

        #center when loaded
        if self._is_first_load:
            self.center_on_svg_items()
            self._is_first_load = False

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

    @Slot(int, int)
    def move_handwriting(self, x: int, y: int):
        if self._current_handwriting:
            self._current_handwriting.move(x, y)
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

    def _on_selection_changed(self):
        #remove old handles
        if self._handles:
            self._scene.removeItem(self._handles)
            self._handles = None

        selected = self._scene.selectedItems()
        #find the HandwritingGroup among selected items
        groups = [i for i in selected if isinstance(i, HandwritingGroup)]
        if groups:
            self._handles = TransformHandles(groups[0])
            self._scene.addItem(self._handles)
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space and not event.isAutoRepeat():
            self._space_held = True
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.viewport().setCursor(Qt.OpenHandCursor)
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space and not event.isAutoRepeat():
            self._space_held = False
            self.setDragMode(QGraphicsView.RubberBandDrag)
            self.viewport().setCursor(Qt.ArrowCursor)
        super().keyReleaseEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            #feed Qt a fake left press to activate hand drag
            fake = QMouseEvent(
                event.type(), event.position(),
                Qt.LeftButton, Qt.LeftButton, event.modifiers()
            )
            super().mousePressEvent(fake)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            if not self._space_held:
                self.setDragMode(QGraphicsView.RubberBandDrag)
            fake = QMouseEvent(
                event.type(), event.position(),
                Qt.LeftButton, Qt.LeftButton, event.modifiers()
            )
            super().mouseReleaseEvent(fake)
        else:
            super().mouseReleaseEvent(event)

    def wheelEvent(self, event: QScrollEvent):
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