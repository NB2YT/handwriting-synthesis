import textwrap
import drawsvg as dw
from typing import List

from PySide6.QtCore import QByteArray, QThread, Signal

from synthesizer_tf2.hand import Hand
from SVG.NotebookPaperGenerator import GenerateNotebookPaperSVG
from SVG.AbsoluteVectorGraphic import AbsoluteVectorGraphic

class HandwritingWorker(QThread):
    finished = Signal(QByteArray)

    def run(self):
        print("loading model")
        self.hand = Hand()
        print("model loaded")

        while True:
            print("worker generating")

            text = "Canada is considered one of the best countries in the world to live in. First, Canada has an excellent health care system, allowing all citizens access to medical services at a reasonable price. Second, Canada has a high standard of education, with students taught by well-trained teachers who encourage university studies. Finally, Canada's cities are clean and efficiently managed, offering many parks and ample space for residents. As a result, Canada is a highly desirable place to live."
        
            lines = textwrap.wrap(text, width=30)
            #max = 2.5 min=0.15
            bias = .75
            #0-12
            style = 12

            generated_lines: List[AbsoluteVectorGraphic] = []
            for line in lines:
                generated_lines.append(self.hand.write(lines=[line], biases=[bias], styles=[style]))


            d = dw.Drawing(1200, 1200)

            g = dw.Group(transform="scale(2)")
            for element in GenerateNotebookPaperSVG().elements:
                g.append(element)
            d.append(g)

            for line in generated_lines:
                for element in line.elements:
                    d.append(element)

            d.save_svg("test.svg")

            #d = self.hand.write(lines=lines, biases=[bias for _ in lines], styles=[style for _ in lines])

            svg_data = QByteArray(d.as_svg().encode('utf-8'))

            #print(d.as_svg())

            self.finished.emit(svg_data)