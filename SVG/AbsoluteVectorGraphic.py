#the point of AVG is to make exported SVGs eaiser to use by external programs like 
#pen plotter softwares. This project was made to easily make handwriting for penplotters.

import drawsvg as dw
from typing import List, Tuple
from abc import ABC, abstractmethod

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

class AbsoluteVectorGraphic():
    def __init__(self):
        self._elements: List[AVGElement] = []

    def append(self, element: AVGElement, offset=(0, 0)):
        element.move(*offset)
        self._elements.append(element)

    def as_drawing(self, size: Tuple[int, int]) -> dw.Drawing:
        drawing = dw.Drawing(size[0], size[1])
        for avg_element in self._elements:
            for dw_element in avg_element.as_drawsvg_elements():
                drawing.append(dw_element)
        return drawing
    
    def export(self, size: Tuple[int, int]) -> str:
        return self.as_drawing(size).as_svg()