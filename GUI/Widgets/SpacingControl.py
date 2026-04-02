from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QSpinBox
from PySide6.QtCore import Qt, Signal

class SpacingControl(QWidget):
    valueChanged = Signal(int)

    def __init__(self, default=60, minimum=10, maximum=200, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        layout.addWidget(QLabel("Line Spacing"))

        row = QHBoxLayout()

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(minimum, maximum)
        self.slider.setValue(default)
        self.slider.setMinimumWidth(80)

        self.spinbox = QSpinBox()
        self.spinbox.setRange(minimum, maximum)
        self.spinbox.setValue(default)

        row.addWidget(self.slider)
        row.addWidget(self.spinbox)
        layout.addLayout(row)

        # Sync slider and spinbox
        self.slider.valueChanged.connect(self.spinbox.setValue)
        self.spinbox.valueChanged.connect(self.slider.setValue)

        # Expose a single valueChanged signal
        self.slider.valueChanged.connect(self.valueChanged)

    def value(self) -> int:
        return self.slider.value()