from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QSpinBox, QDoubleSpinBox
from PySide6.QtCore import Signal, Qt

from SVG.NotebookPaperGenerator import NotebookPaper

class NotebookPaperControls(QWidget):
    valueChanged = Signal(NotebookPaper)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        form = QFormLayout()
        form.setSpacing(8)

        self._width       = self._spinbox(1, 1000, 210)
        self._height      = self._spinbox(1, 1000, 297)
        self._top_margin  = self._spinbox(0, 500, 20)
        self._left_margin = self._spinbox(0, 500, 20)
        self._line_count  = self._spinbox(1, 100, 20)
        self._h_thickness = self._double_spinbox(0.1, 10.0, 0.5)
        self._v_thickness = self._double_spinbox(0.1, 10.0, 0.5)

        form.addRow("Width (mm)",            self._width)
        form.addRow("Height (mm)",           self._height)
        form.addRow("Top Margin (mm)",       self._top_margin)
        form.addRow("Left Margin (mm)",      self._left_margin)
        form.addRow("Line Count",            self._line_count)
        form.addRow("H. Thickness",          self._h_thickness)
        form.addRow("V. Thickness",          self._v_thickness)

        layout.addLayout(form)

    def _spinbox(self, minimum: int, maximum: int, default: int) -> QSpinBox:
        spinbox = QSpinBox()
        spinbox.setRange(minimum, maximum)
        spinbox.setValue(default)
        spinbox.valueChanged.connect(self._emit)
        return spinbox
    
    def _double_spinbox(self, minimum: float, maximum: float, default: float) -> QDoubleSpinBox:
        spinbox = QDoubleSpinBox()
        spinbox.setRange(minimum, maximum)
        spinbox.setSingleStep(0.1)
        spinbox.setValue(default)
        spinbox.valueChanged.connect(self._emit)
        return spinbox
    
    def _emit(self):
        self.valueChanged.emit(self.value())

    def value(self):
        return NotebookPaper(
            width=self._width.value(),
            height=self._height.value(),
            top_margin=self._top_margin.value(),
            left_margin=self._left_margin.value(),
            horizontal_line_count=self._line_count.value(),
            horizontal_line_thickness=self._h_thickness.value(),
            vertical_line_thickness=self._v_thickness.value(),
        )
            