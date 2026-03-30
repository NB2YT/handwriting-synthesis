import drawsvg as dw
from typing import List, Tuple
from abc import ABC, abstractmethod

class AbsoluteVectorGraphic():
    def __init__(self):
        self._elements: List[dw.DrawingElement] = []

    def append(self, drawing: dw.Drawing, offset: Tuple[int, int]=(0, 0)):
        group = dw.Group()
        for element in drawing.elements:
            element.args["x"] += offset[0]
            element.args["y"] += offset[1]
            group.append(element)
        self._elements.append(group)
        return group

    def export(self, size: Tuple[int, int]) -> str:
        drawing = dw.Drawing(size[0], size[1])
        for element in self._elements:
            drawing.append(element)
        return drawing.as_svg()
    
class AVGElement(ABC):
    def __init__(self, id=""):
        self._elements = dw.Group(id=id)

    @abstractmethod
    def move(self, x, y):
        pass

    @property
    @abstractmethod
    def elements(self) -> List[dw.DrawingElement]:
        pass