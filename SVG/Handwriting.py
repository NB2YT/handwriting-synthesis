import drawsvg as dw
from dataclasses import dataclass
from typing import Literal, List
import warnings
import functools

from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItem
from PySide6.QtGui import QPainterPath, QColor, QPen, QBrush
from PySide6.QtCore import Qt

from SVG.AbsoluteVectorGraphic import AVGElement
from SVG.Transform.HandwritingGroup import HandwritingGroup

@dataclass
class HandwritingPathMovement:
    method: Literal['M', "L"]
    x: int
    y: int

class HandwritingLine(AVGElement):
    def __init__(self, color, width):
        self._movements: List[HandwritingPathMovement] = []
        self._color = color
        self._width = width
        self._linecap = "round"
        self._fill = "none"

    def __repr__(self):
        return f"HandwritingLine: {len(self._movements)} movements"

    #relative
    def move(self, x, y):
        for movement in self._movements:
            movement.x += x
            movement.y += y

    #absolute
    #equivilent to the M method in SVG paths
    def start_feature(self, x, y):
        self._movements.append(HandwritingPathMovement(method="M", x=x, y=y))

    #absolute
    #equivilent to the L method in SVG paths
    def continue_feature(self, x, y):
        self._movements.append(HandwritingPathMovement(method="L", x=x, y=y))

    def as_path(self) -> dw.Path:
        path = dw.Path(stroke=self._color, stroke_width=self._width, linecap=self._linecap, fill=self._fill)
        for movement in self._movements:
            if movement.method == "M":
                path.M(movement.x, movement.y)
            elif movement.method == "L":
                path.L(movement.x, movement.y)
        return path
    
    def as_drawsvg_elements(self):
        return [self.as_path()]
    
    def as_graphics_items(self) -> List[QGraphicsItem]:
        path = QPainterPath()
        for movement in self._movements:
            if movement.method == "M":
                path.moveTo(movement.x, movement.y)
            elif movement.method == "L":
                path.lineTo(movement.x, movement.y)
        
        item = QGraphicsPathItem(path)
        pen = QPen(QColor(self._color), self._width)
        pen.setCapStyle(Qt.RoundCap)
        item.setPen(pen)
        item.setBrush(QBrush(Qt.NoBrush))
        return [item]

@dataclass
class HandwritingTransformConfig:
    scale: float
    spacing: float
    x_offset: int
    y_offset: int

#TODO: add pydantic validation
@dataclass
class HandwritingGenerationConfig:
    text: str
    line_width: int
    bias: float #0.15-2.5
    style: int #0-12

class Handwriting(AVGElement):
    def __init__(self):
        self._lines: List[HandwritingLine] = []
        self._finished = False

        #transforms
        self._current_spacing = 0
        self._current_scale = 1
        self._current_x = 0
        self._current_y = 0

    def __len__(self):
        return len(self._lines)
    
    def __repr__(self):
        str = f"Handwriting with {len(self)} lines:"
        for line in self._lines:
            str += f"\n  {line}"
        return str

    # --- Generation ---
    def append_line(self, line: HandwritingLine):
        self._lines.append(line)
    
    def finish(self):
        #the handwriting has been fully generated and transformations can now be applied to it.
        self._finished = True
    
    # --- Transforms ---
    @staticmethod
    def _transformation(func):
        #preserve the original function's name and docstring for better debugging.
        @functools.wraps(func)

        #give a warning if a transformation function is called before the handwriting is finished.
        def wrapper(self, *args, **kwargs):
            if not self._finished:
                warnings.warn("Applying a transformation to a handwriting that has not been finished yet may cause unexpected results.")
            return func(self, *args, **kwargs)
        return wrapper

    @_transformation
    def move(self, x, y):
        self._current_x += x
        self._current_y += y
        for line in self._lines:
            line.move(x, y)

    @_transformation
    def set_position(self, x, y):
        relative_x = x - self._current_x
        relative_y = y - self._current_y
        self.move(relative_x, relative_y)

    @_transformation
    def set_spacing(self, spacing):
        relative_spacing = spacing - self._current_spacing
        for i, line in enumerate(self._lines):
            line.move(0, relative_spacing * i)
        self._current_spacing += relative_spacing

    @_transformation
    def set_scale(self, scale):
        relative_scale = scale / self._current_scale

        #find center of handwriting
        all_x = [movement.x for line in self._lines for movement in line._movements]
        all_y = [movement.y for line in self._lines for movement in line._movements]
        center_x = (min(all_x) + max(all_x)) / 2
        center_y = (min(all_y) + max(all_y)) / 2

        for line in self._lines:
            for movement in line._movements:
                movement.x = center_x + (movement.x - center_x) * relative_scale
                movement.y = center_y + (movement.y - center_y) * relative_scale
        
        self._current_scale = scale

    def apply_config(self, config: HandwritingTransformConfig):
        self.set_scale(config.scale)
        self.set_spacing(config.spacing)
        self.set_position(config.x_offset, config.y_offset)

    # --- Export ---
    def as_group(self) -> dw.Group:
        group = dw.Group(id="handwriting")
        for line in self._lines:
            group.append(line.as_path())
        return group
    
    def as_drawsvg_elements(self) -> List[dw.DrawingElement]:
        return [self.as_group()]
    
    def as_graphics_items(self) -> List[QGraphicsItem]:
        group = HandwritingGroup(self)
        for line in self._lines:
            for item in line.as_graphics_items():
                group.addToGroup(item)
        return [group]
