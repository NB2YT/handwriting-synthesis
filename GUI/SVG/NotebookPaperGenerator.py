from drawsvg import Drawing, Rectangle, Use

#millimeters
def GenerateNotebookPaperSVG() -> Drawing:
    width = 200
    height = 600
    top_margin = 30
    left_margin = 40
    horizontal_line_count = 26
    horizontal_line_thickness = 0.6
    vertical_line_thickness = 0.6

    d = Drawing(width, height, id_prefix="notebook_paper")

    paper = Rectangle(0, 0, width, height, fill="white")
    d.append(paper)

    vertical_line = Rectangle(left_margin, 0, vertical_line_thickness, height, fill="red")
    d.append(vertical_line)

    #horizontal lines
    horizontal_line_reference = Rectangle(0, 0, width, horizontal_line_thickness, fill="blue")
    spacing = (height - top_margin) / horizontal_line_count
    for i in range(horizontal_line_count):
        y = top_margin + (spacing * i)
        horizontal_line = Use(horizontal_line_reference, 0, y)
        d.append(horizontal_line)

    return d