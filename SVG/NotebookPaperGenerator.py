import drawsvg as dw

from SVG.AbsoluteVectorGraphic import AVGElementAdapter
from SVG.Units import Millimeter as mm

class NotebookPaper(AVGElementAdapter):
    #unit = millimeters
    def __init__(self, width, height, top_margin, left_margin, horizontal_line_count, horizontal_line_thickness, vertical_line_thickness):
        self.width = mm(width)
        self.height = mm(height)
        self.top_margin = mm(top_margin)
        self.left_margin = mm(left_margin)
        self.horizontal_line_count = horizontal_line_count
        self.horizontal_line_thickness = mm(horizontal_line_thickness)
        self.vertical_line_thickness = mm(vertical_line_thickness)

    def as_group(self) -> dw.Group:
        group = dw.Group(id="notebook_paper")

        paper = dw.Rectangle(0, 0, self.width, self.height, fill="white")
        group.append(paper)

        vertical_line = dw.Rectangle(self.left_margin, 0, self.vertical_line_thickness, self.height, fill="red")
        group.append(vertical_line)

        #horizontal lines
        horizontal_lines = dw.Group(id="horizontal_lines")
        spacing = (self.height - self.top_margin) / self.horizontal_line_count
        for i in range(self.horizontal_line_count):
            y = self.top_margin + (spacing * i)
            horizontal_line = dw.Rectangle(0, y, self.width, self.horizontal_line_thickness, fill="blue")
            horizontal_lines.append(horizontal_line)
        group.append(horizontal_lines)

        return group

    def as_drawsvg_elements(self):
        return [self.as_group()]

