import drawsvg as dw
from dataclasses import dataclass
from typing import Literal, List

from SVG.AbsoluteVectorGraphic import AVGElement

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


class Handwriting(AVGElement):
    def __init__(self, line_height):
        self._lines: List[HandwritingLine] = []
        self._line_height = line_height

        #transforms
        self._cumulative_spacing = 0

    def __len__(self):
        return len(self._lines)
    
    def __repr__(self):
        str = ""
        str += f"Handwriting with {len(self)} lines:"
        for line in self._lines:
            str += f"\n  {line}"
        return str

    def append_line(self, line: HandwritingLine):
        self._lines.append(line)

    def move(self, x, y):
        for line in self._lines:
            line.move(x, y)

    def set_spacing(self, spacing):
        relative_spacing = spacing - self._cumulative_spacing
        for i, line in enumerate(self._lines):
            line.move(0, relative_spacing * i)

    
    def as_group(self) -> dw.Group:
        group = dw.Group(id="handwriting")
        for line in self._lines:
            group.append(line.as_path())
        return group
    
    def as_drawsvg_elements(self):
        return [self.as_group()]