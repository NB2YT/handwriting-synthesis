from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QSpinBox, QDoubleSpinBox
from PySide6.QtCore import Signal, Qt

from SVG.Handwriting import HandwritingConfig

from GUI.Widgets.Templates.LabeledSliderSpinBox import LabeledSliderDoubleSpinBox

class HandwritingControls(QWidget):
    valueChanged = Signal(HandwritingConfig)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self._scale_control = LabeledSliderDoubleSpinBox(
            default=1,
            minimum=.01,
            maximum=10,
            step=0.01,
            label="Scale"
        )
        layout.addWidget(self._scale_control)
        self._scale_control.valueChanged.connect(self._emit)

        self._spacing_control = LabeledSliderDoubleSpinBox(
            default=60,
            minimum=0,
            maximum=500,
            step=0.1,
            label="Spacing (mm)"
        )
        layout.addWidget(self._spacing_control)
        self._spacing_control.valueChanged.connect(self._emit)
    
    def _emit(self):
        self.valueChanged.emit(self.value())

    def value(self):
        return HandwritingConfig(
            spacing=self._spacing_control.value(),
            scale=self._scale_control.value()
        )