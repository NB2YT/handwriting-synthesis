import sys
from PyQt5.QtWidgets import QApplication

from GUI import Application

if __name__ == "__main__":
    from SVG.NotebookPaperGenerator import GenerateNotebookPaperSVG
    #print(GenerateNotebookPaperSVG().as_svg())
    from SVG.AbsoluteVectorGraphic import AbsoluteVectorGraphic
    avg = AbsoluteVectorGraphic()
    avg.append(GenerateNotebookPaperSVG(), offset=(100, 300))
    print(avg.export(size=(1000, 1000)))

    app = QApplication(sys.argv)
    viewer = Application.MainWindow()
    viewer.show()
    sys.exit(app.exec_())