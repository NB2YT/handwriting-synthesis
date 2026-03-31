import drawsvg as dw

from SVG.AbsoluteVectorGraphic import AVGElementAdapter

class NotebookPaper(AVGElementAdapter):
    #unit = millimeters
    def __init__(self, width, height, top_margin, left_margin, horizontal_line_count, horizontal_line_thickness, vertical_line_thickness):
        self.width = width
        self.height = height
        self.top_margin = top_margin
        self.left_margin = left_margin
        self.horizontal_line_count = horizontal_line_count
        self.horizontal_line_thickness = horizontal_line_thickness
        self.vertical_line_thickness = vertical_line_thickness
        
        super().__init__([self._generate()])

    def _generate(self) -> dw.Group:
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

    def as_group(self) -> dw.Group:
        return self._elements[0]

