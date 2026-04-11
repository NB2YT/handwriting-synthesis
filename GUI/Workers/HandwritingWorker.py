import textwrap
from queue import Queue

from PySide6.QtCore import QThread, Signal, Slot

from synthesizer_tf2.hand import Hand
from SVG.Handwriting import Handwriting, HandwritingGenerationConfig

class HandwritingWorker(QThread):
    finished = Signal(Handwriting)
    processing = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setObjectName("Handwriting Generator")
        self._queue = Queue()

    def run(self):
        print("loading model")
        self.hand = Hand()
        print("model loaded")

        while True:
            config: HandwritingGenerationConfig = self._queue.get()
            if config is None:
                break

            print("worker generating")
            self.processing.emit(True)
            lines = textwrap.wrap(config.text, width=config.line_width)
            handwriting = self.hand.write(
                lines=lines,
                biases=[config.bias] * len(lines),
                styles=[config.style] * len(lines)
            )
            self.processing.emit(False)
            self.finished.emit(handwriting)

    @Slot(HandwritingGenerationConfig)
    def generate(self, config: HandwritingGenerationConfig):
        self._queue.put(config)
    
    def stop(self):
        self._queue.put(None)
        self.wait()