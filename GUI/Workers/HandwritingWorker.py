import textwrap

from PyQt5.QtCore import QByteArray, QThread, pyqtSignal

from synthesizer.hand import Hand

from GUI.SVG.NotebookPaperGenerator import GenerateNotebookPaperSVG

class HandwritingWorker(QThread):
    finished = pyqtSignal(QByteArray)

    def run(self):
        print("loading model")
        self.hand = Hand()
        print("model loaded")

        while True:
            print("worker generating")

            text = "Canada is considered one of the best countries in the world to live in. First, Canada has an excellent health care system, allowing all citizens access to medical services at a reasonable price. Second, Canada has a high standard of education, with students taught by well-trained teachers who encourage university studies. Finally, Canada's cities are clean and efficiently managed, offering many parks and ample space for residents. As a result, Canada is a highly desirable place to live."
        
            lines = textwrap.wrap(text, width=30)
            #max = 2.5 min=0.15
            biases = [0.75 for i in lines]
            #0-12
            styles = [7 for i in lines]

            svg = self.hand.write(
                lines=lines,
                biases=biases,
                styles=styles,
            )

            svg.add(GenerateNotebookPaperSVG())

            svg_data = QByteArray(svg.tostring().encode('utf-8'))

            self.finished.emit(svg_data)