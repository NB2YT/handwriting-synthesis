#the point of AVG is to make exported SVGs eaiser to use by external programs like 
#pen plotter softwares. This project was made to easily make handwriting for penplotters.

import drawsvg as dw
from typing import List, Tuple
from abc import ABC, abstractmethod

from PySide6.QtWidgets import QGraphicsItem, QGraphicsRectItem
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtCore import Qt

class AVGElement(ABC):
    @abstractmethod
    def __init__(self, id=""):
        pass

    #relative
    @abstractmethod
    def move(self, x, y) -> None:
        pass

    @abstractmethod
    def as_drawsvg_elements(self) -> List[dw.DrawingElement]:
        pass

    @abstractmethod
    def as_graphics_items(self) -> List[QGraphicsItem]:
        pass


#generic wrapper for drawsvg elements to be used in the AbsoluteVectorGraphic. 
#This only works with elements that use x and y args for their position, 
#but this includes some of the basic shapes (rect, circle).
#any element that is path based cannot use this wrapper
class AVGElementAdapter(AVGElement):
    def __init__(self, elements: List[dw.DrawingElement]):
        self._elements: List[dw.DrawingElement] = elements


    def _move_element(self, element: dw.DrawingElement, x, y):
        if isinstance(element, dw.DrawingParentElement):
            for child in element.children:
                self._move_element(child, x, y)
        
        #paths are a special case because they use a list of commands instead of x and y args
        elif isinstance(element, dw.Path):
            raise Exception("Path elements cannot be used with the AVGElementAdapter. Please create a custom adapter for path elements.")
        
        #everything else that has x and y args
        elif isinstance(element, dw.DrawingBasicElement):
            element.args["x"] += x
            element.args["y"] += y

    #relative
    def move(self, x, y):
        for element in self._elements:
            self._move_element(element, x, y)

    def as_drawsvg_elements(self) -> List[dw.DrawingElement]:
        return self._elements
    
    def _dw_element_to_graphics_items(self, element) -> List[QGraphicsItem]:
        items = []

        if isinstance(element, dw.Group):
            for child in element.children:
                items.extend(self._dw_element_to_graphics_items(child))
        
        elif isinstance(element, dw.Rectangle):
            x       = float(element.args["x"])
            y       = float(element.args["y"])
            width   = float(element.args["width"])
            height  = float(element.args["height"])
            fill    = element.args["fill"]

            item = QGraphicsRectItem(x, y, width, height)
            item.setBrush(QBrush(QColor(fill)))
            item.setPen(QPen(Qt.NoPen))
            items.append(item)

        return items

    def as_graphics_items(self) -> List[QGraphicsItem]:
        items = []
        for element in self._elements:
            items.extend(self._dw_element_to_graphics_items(element))
        return items

class AbsoluteVectorGraphic():
    def __init__(self):
        self._elements: List[AVGElement] = []

    def append(self, element: AVGElement, offset=(0, 0)):
        element.move(*offset)
        self._elements.append(element)

    def prepend(self, element: AVGElement, offset=(0, 0)):
        element.move(*offset)
        self._elements.insert(0, element)

    def as_drawing(self, size: Tuple[int, int]) -> dw.Drawing:
        drawing = dw.Drawing(size[0], size[1])
        for avg_element in self._elements:
            drawing.extend(avg_element.as_drawsvg_elements())
        return drawing
    
    def as_graphics_items(self) -> List[QGraphicsItem]:
        items = []
        for avg_element in self._elements:
            items.extend(avg_element.as_graphics_items())
        return items
    
    def as_svg(self, size: Tuple[int, int]) -> str:
        return self.as_drawing(size).as_svg()