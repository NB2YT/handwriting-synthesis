import sys
from PySide6.QtWidgets import QApplication

from GUI import Application

if __name__ == "__main__":
    #from SVG.NotebookPaperGenerator import GenerateNotebookPaperAVG
    #print(GenerateNotebookPaperSVG().as_svg())
    from SVG.AbsoluteVectorGraphic import AbsoluteVectorGraphic
    avg = AbsoluteVectorGraphic()
    #avg.append(GenerateNotebookPaperAVG(), offset=(100, 300))
    print(avg.as_svg(size=(1000, 1000)))

    app = QApplication(sys.argv)
    viewer = Application.MainWindow()
    viewer.show()
    sys.exit(app.exec_())