import sys
from PySide6.QtWidgets import QApplication

from GUI import Application

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = Application.MainWindow()
    viewer.show()
    sys.exit(app.exec())