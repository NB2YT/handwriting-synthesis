import textwrap
import drawsvg as dw
from typing import List

from PySide6.QtCore import QByteArray, QThread, Signal

from synthesizer_tf2.hand import Hand
from SVG.NotebookPaperGenerator import NotebookPaper
from SVG.AbsoluteVectorGraphic import AbsoluteVectorGraphic, AVGElementAdapter
from SVG.Handwriting import Handwriting

class HandwritingWorker(QThread):
    finished = Signal(Handwriting)

    def __init__(self):
        super().__init__()
        self.setObjectName("Handwriting Generator")

    def run(self):
        print("loading model")
        self.hand = Hand()
        print("model loaded")

        while True:
            print("worker generating")

            text = "Canada is considered one of the best countries in the world to live in. First, Canada has an excellent health care system, allowing all citizens access to medical services at a reasonable price. Second, Canada has a high standard of education, with students taught by well-trained teachers who encourage university studies. Finally, Canada's cities are clean and efficiently managed, offering many parks and ample space for residents. As a result, Canada is a highly desirable place to live."
        
            lines = textwrap.wrap(text, width=30)
            #max = 2.5 min=0.15
            bias = 2.5
            #0-12
            style = 12
            stroke_width = 1

            handwriting = self.hand.write(
                lines=lines, 
                biases=[bias]*len(lines), 
                styles=[style]*len(lines), 
                stroke_widths=[stroke_width]*len(lines)
            )
            print(handwriting)

            #avg = AbsoluteVectorGraphic()
            #avg.append(AVGElementAdapter([dw.Rectangle(0, 0, 1000, 1000, fill="white")]))
            #avg.append(NotebookPaper(width=210, height=297, top_margin=20, left_margin=20, horizontal_line_count=20, horizontal_line_thickness=0.5, vertical_line_thickness=0.5))
            #avg.append(handwriting)
            handwriting.set_spacing(60)

            #avg.as_drawing(size=("1000mm", "1000mm")).save_svg("test.svg")

            self.finished.emit(handwriting)