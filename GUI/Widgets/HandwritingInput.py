from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit,
    QPushButton, QLabel, QSizePolicy
)
from PySide6.QtCore import Signal, Qt

from SVG.Handwriting import HandwritingGenerationConfig
from GUI.Widgets.Templates.LabeledSliderSpinBox import LabeledSliderDoubleSpinBox, LabeledSliderSpinBox

class HandwritingInput(QWidget):
    valueChanged = Signal(HandwritingGenerationConfig)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        layout.addWidget(QLabel("Text"))

        self._text_edit = QPlainTextEdit()
        self._text_edit.setPlaceholderText("Enter text to synthesize...")
        self._text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._text_edit.setMinimumHeight(120)
        layout.addWidget(self._text_edit)

        self._bias_control = LabeledSliderDoubleSpinBox(
            default=0.75,
            minimum=0.15,
            maximum=2.5,
            step=0.1,
            label="Bias (Legibility)"
        )
        layout.addWidget(self._bias_control)

        self._style_control = LabeledSliderSpinBox(
            default=7,
            minimum=0,
            maximum=12,
            step=1,
            label="Style"
        )
        layout.addWidget(self._style_control)

        self._line_width_control = LabeledSliderSpinBox(
            default=30,
            minimum=1,
            maximum=100,
            step=5,
            label="Line width (Character per line)"
        )
        layout.addWidget(self._line_width_control)

        button_row = QHBoxLayout()
        button_row.setSpacing(8)

        self._char_count = QLabel("0 chars")
        self._char_count.setStyleSheet("color: gray; font-size: 11px;")
        button_row.addWidget(self._char_count, alignment=Qt.AlignVCenter)
        button_row.addStretch()

        self._generate_btn = QPushButton("Generate")
        self._generate_btn.setFixedWidth(80)
        self._generate_btn.clicked.connect(self._emit)
        button_row.addWidget(self._generate_btn)

        layout.addLayout(button_row)

        self._text_edit.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self):
        count = len(self._text_edit.toPlainText())
        self._char_count.setText(f"{count} chars")

    def _emit(self):
        self.valueChanged.emit(self.value())

    def value(self) -> HandwritingGenerationConfig:
        return HandwritingGenerationConfig(
            text=self._text_edit.toPlainText(),
            line_width=self._line_width_control.value(),
            bias=self._bias_control.value(),
            style=self._style_control.value()
        )