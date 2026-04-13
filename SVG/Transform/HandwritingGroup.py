from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsItem
from PySide6.QtCore import QPointF

import SVG

class HandwritingGroup(QGraphicsItemGroup):
    def __init__(self, handwriting: "SVG.Handwriting"):
        super().__init__()
        self._handwriting = handwriting
        self._last_pos = QPointF(0, 0)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            delta = value - self._last_pos
            self._last_pos = value
            # keep data model in sync for SVG export
            self._handwriting.move(delta.x(), delta.y())
        return super().itemChange(change, value)