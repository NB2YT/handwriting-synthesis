from enum import IntEnum

from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
from PySide6.QtCore import Qt, QRectF, QPointF

from SVG.Transform.HandwritingGroup import HandwritingGroup

class Handle(IntEnum):
    TOP_LEFT     = 0
    TOP_CENTER   = 1
    TOP_RIGHT    = 2
    MID_LEFT     = 3
    MID_RIGHT    = 4
    BOT_LEFT     = 5
    BOT_CENTER   = 6
    BOT_RIGHT    = 7

HANDLE_SIZE = 8

class TransformHandles(QGraphicsItem):
    def __init__(self, group: HandwritingGroup):
        super().__init__()
        self._group = group
        self._drag_handle: Handle | None = None
        self._drag_start_pos = QPointF()
        self._drag_start_rect = QRectF()
        self.setZValue(1000)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)

    def _content_rect(self) -> QRectF:
        #bounding rect in scene coords, converted to our local coords
        return self.mapRectFromScene(
            self._group.mapToScene(
                self._group.boundingRect()
            ).boundingRect()
        )

    def _handle_rects(self) -> dict[Handle, QRectF]:
        r = self._content_rect()
        s = HANDLE_SIZE
        cx, cy = r.center().x(), r.center().y()
        positions = {
            Handle.TOP_LEFT:    QPointF(r.left(),  r.top()),
            Handle.TOP_CENTER:  QPointF(cx,         r.top()),
            Handle.TOP_RIGHT:   QPointF(r.right(),  r.top()),
            Handle.MID_LEFT:    QPointF(r.left(),   cy),
            Handle.MID_RIGHT:   QPointF(r.right(),  cy),
            Handle.BOT_LEFT:    QPointF(r.left(),   r.bottom()),
            Handle.BOT_CENTER:  QPointF(cx,          r.bottom()),
            Handle.BOT_RIGHT:   QPointF(r.right(),  r.bottom()),
        }
        return {
            h: QRectF(p.x() - s/2, p.y() - s/2, s, s)
            for h, p in positions.items()
        }

    def boundingRect(self) -> QRectF:
        return self._content_rect().adjusted(-HANDLE_SIZE, -HANDLE_SIZE,
                                              HANDLE_SIZE,  HANDLE_SIZE)

    def paint(self, painter: QPainter, option, widget=None):
        painter.save()
        # dashed bounding rect
        pen = QPen(QColor("#4A90D9"), 1, Qt.DashLine)
        pen.setDashPattern([4, 4])
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self._content_rect())

        #handles
        painter.setPen(QPen(QColor("#4A90D9"), 1))
        painter.setBrush(QBrush(QColor("white")))
        for rect in self._handle_rects().values():
            painter.drawRect(rect)
        painter.restore()

    def _handle_at(self, pos: QPointF) -> Handle | None:
        for handle, rect in self._handle_rects().items():
            if rect.contains(pos):
                return handle
        return None

    def mousePressEvent(self, event):
        handle = self._handle_at(event.pos())
        if handle is not None:
            self._drag_handle = handle
            self._drag_start_pos = event.scenePos()
            self._drag_start_rect = self._group.mapToScene(
                self._group.boundingRect()
            ).boundingRect()
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if self._drag_handle is None:
            return
        delta = event.scenePos() - self._drag_start_pos
        r = self._drag_start_rect
        new_rect = QRectF(r)

        h = self._drag_handle
        if h in (Handle.TOP_LEFT, Handle.MID_LEFT, Handle.BOT_LEFT):
            new_rect.setLeft(r.left() + delta.x())
        if h in (Handle.TOP_RIGHT, Handle.MID_RIGHT, Handle.BOT_RIGHT):
            new_rect.setRight(r.right() + delta.x())
        if h in (Handle.TOP_LEFT, Handle.TOP_CENTER, Handle.TOP_RIGHT):
            new_rect.setTop(r.top() + delta.y())
        if h in (Handle.BOT_LEFT, Handle.BOT_CENTER, Handle.BOT_RIGHT):
            new_rect.setBottom(r.bottom() + delta.y())

        if new_rect.width() < 10 or new_rect.height() < 10:
            return

        sx = new_rect.width()  / r.width()
        sy = new_rect.height() / r.height()
        scale = min(sx, sy)  #uniform scale

        transform = self._group.transform()
        transform.scale(scale / (transform.m11() or 1),
                        scale / (transform.m22() or 1))
        self._group.setTransform(transform)

        self.prepareGeometryChange()
        event.accept()

    def mouseReleaseEvent(self, event):
        if self._drag_handle is not None:
            #sync final scale to data model
            t = self._group.transform()
            self._group._handwriting.set_scale(t.m11())
            self._drag_handle = None
        event.accept()