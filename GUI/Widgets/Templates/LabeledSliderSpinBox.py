from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSlider,
    QDoubleSpinBox
)
from PySide6.QtCore import Signal, Qt

class LabeledSliderDoubleSpinBox(QWidget):
    valueChanged = Signal(float)

    def __init__(self, default: float, minimum: float, maximum: float, step: float, label: str, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        layout.addWidget(QLabel(label))

        row = QHBoxLayout()

        self._factor = round(1 / step)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(round(minimum * self._factor), round(maximum * self._factor))
        self.slider.setValue(round(default * self._factor))

        self.spinbox = QDoubleSpinBox()
        self.spinbox.setRange(minimum, maximum)
        self.spinbox.setSingleStep(step)
        self.spinbox.setValue(default)
        self.spinbox.setMinimumWidth(
            self.spinbox.fontMetrics().horizontalAdvance(str(maximum)) + 30
        )

        row.addWidget(self.slider)
        row.addWidget(self.spinbox)
        layout.addLayout(row)

        #sync slider and spinbox
        self.slider.valueChanged.connect(lambda v: self.spinbox.setValue(v / self._factor))
        self.spinbox.valueChanged.connect(lambda v: self.slider.setValue(round(v * self._factor)))

        self.spinbox.valueChanged.connect(self.valueChanged)

    def value(self) -> float:
        return self.spinbox.value()