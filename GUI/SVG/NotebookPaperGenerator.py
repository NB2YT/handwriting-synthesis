import svgwrite

#millimeters
def GenerateNotebookPaperSVG() -> svgwrite.Drawing:
    width = 200
    height = 600
    top_margin = 30
    left_margin = 40
    horizontal_line_count = 26
    horizontal_line_thickness = 0.6
    vertical_line_thickness = 0.6

    dwg = svgwrite.Drawing()

    #paper
    dwg.add(dwg.rect(
        insert=(0, 0), 
        size=(width, height), 
        fill='white'
    ))

    #vertical line
    dwg.add(dwg.rect(
        insert=(left_margin, 0), 
        size=(vertical_line_thickness, height),
        fill='red'
    ))

    #horizontal lines
    spacing = (height - top_margin) / horizontal_line_count
    for i in range(horizontal_line_count):
        y = top_margin + spacing * i
        dwg.add(dwg.rect(
            insert=(0, y),
            size=(width, horizontal_line_thickness),
            fill='blue'
        ))

    return dwg