import sys
from PyQt5.QtWidgets import QApplication

from GUI import Application

if __name__ == "__main__":
    from GUI.SVG.NotebookPaperGenerator import GenerateNotebookPaperSVG
    print(GenerateNotebookPaperSVG().as_svg())

    app = QApplication(sys.argv)
    viewer = Application.MainWindow()
    viewer.show()
    sys.exit(app.exec_())