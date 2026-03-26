import sys
import textwrap

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtCore import QByteArray, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPainter

from synthesizer import hand
from synthesizer.hand import Hand

class SVGWorker(QThread):
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

            svg_data = QByteArray(svg.tostring().encode('utf-8'))

            self.finished.emit(svg_data)

class SVGZoomView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        #allow panning
        self.scene.setSceneRect(-5000, -5000, 10000, 10000)
        self.centerOn(0, 0)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Enable dragging/panning with the left mouse button
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        # Smooth out the rendering
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)

        self.svg_item = None
        self.renderer = None
        
        self.worker = SVGWorker()
        self.worker.finished.connect(self.apply_svg)
        self.worker.start()

    def apply_svg(self, svg_data):
        self.renderer = QSvgRenderer(svg_data)

        if self.svg_item:
            self.scene.removeItem(self.svg_item)

        self.svg_item = QGraphicsSvgItem()
        self.svg_item.setSharedRenderer(self.renderer)
        self.scene.addItem(self.svg_item)

    def wheelEvent(self, event):
        # Zoom Factor
        zoom_in = 1.25
        zoom_out = 1 / zoom_in

        # Check wheel direction
        if event.angleDelta().y() > 0:
            self.scale(zoom_in, zoom_in)
        else:
            self.scale(zoom_out, zoom_out)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pro SVG Zoomer")
        self.resize(800, 600)
        
        self.viewer = SVGZoomView()
        self.setCentralWidget(self.viewer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MainWindow()
    viewer.show()
    sys.exit(app.exec_())