import sys
import time

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator, QValidator
from PyQt6.QtCore import QRegularExpression

import can_crc


class CRCWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalkulator CRC CAN")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        sequence_label = QLabel("Bity:")
        self.sequence_regexp = QRegularExpression("[0-1]{96}}")
        self.sequence_input = QLineEdit()
        self.sequence_input.setValidator(QRegularExpressionValidator(self.sequence_regexp))

        layout.addWidget(sequence_label)
        layout.addWidget(self.sequence_input)

        repeat_label = QLabel("Liczba powtórzeń:")
        self.repeat_regexp = QRegularExpression("[0-9]*")
        self.repeat_input = QLineEdit()
        self.repeat_input.setValidator(QIntValidator(1,10**9))
        layout.addWidget(repeat_label)
        layout.addWidget(self.repeat_input)

        self.calculate_button = QPushButton("START")
        self.calculate_button.clicked.connect(self.calculate_crc)
        layout.addWidget(self.calculate_button)

        self.result_label1 = QLabel()
        self.result_label2 = QLabel()
        self.result_label3 = QLabel()
        layout.addWidget(self.result_label1)
        layout.addWidget(self.result_label2)
        layout.addWidget(self.result_label3)

        self.setLayout(layout)

    def input_clear(self):
        self.result_label1.clear()
        self.result_label2.clear()
        self.result_label3.clear()

    def calculate_crc(self):
        self.input_clear()
        data = self.sequence_input.text().replace(" ", "")

        if self.repeat_input.text() == '':
            self.result_label1.setText('Błędne dane')
            return

        repeats = int(self.repeat_input.text())

        bits = can_crc.bitStringToByteArray(data)

        start_time = time.time() * 1000
        for _ in range(repeats):
            crc = can_crc.calculate_crc(bits)
        end_time = time.time() * 1000
        total_time = (end_time - start_time)

        self.result_label1.setText(f"Czas całkowity: {total_time:.8f}ms")
        self.result_label2.setText(f"Czas 1 iteracji: {total_time/repeats:.8f}ms")
        self.result_label3.setText("CRC: " + crc.upper())

    def run(self):
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    crc_widget = CRCWidget()
    crc_widget.run()
    sys.exit(app.exec())