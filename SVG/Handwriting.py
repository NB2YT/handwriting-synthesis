import drawsvg as dw
from dataclasses import dataclass
from typing import Literal, List

@dataclass
class HandwritingPathMovement:
    method: Literal['M', "L"]
    x: int
    y: int

class HandwritingLine:
    def __init__(self):
        self._movements: List[HandwritingPathMovement] = []

    #relative
    def move(self, x, y):
        for movement in self._movements:
            movement.x += x
            movement.y += y

    def as_path(self) -> dw.Path:
        path = dw.Path()
        for movement in self._movements:
            if movement.method == "M":
                path.M(movement.x, movement.y)
            elif movement.method == "L":
                path.L(movement.x, movement.y)
        return [path]


class Handwriting:
    def __init__(self):
        self._lines: List[HandwritingLine] = []

    def __len__(self):
        return len(self._lines)

    def append_line(self, line: HandwritingLine):
        self._lines.append(line)

    def move(self, x, y):
        for line in self._lines:
            line.move(x, y)
    
    def as_group(self) -> dw.Group:
        group = dw.Group(id="handwriting")
        for line in self._lines:
            group.append(line.as_path())
        return group