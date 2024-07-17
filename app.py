import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QMessageBox, QTextEdit, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont, QColor
from enigma import enigma


class EnigmaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Enigma Machine Emulator")
        self.setGeometry(100, 100, 1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        input_layout = QVBoxLayout()
        
        self.input_message = QLineEdit(self)
        self.input_message.setPlaceholderText("Enter message here")
        self.input_message.setFixedSize(800, 50)
        self.input_message.setStyleSheet(self.input_style())
        input_layout.addWidget(self.input_message)

        self.rotor_position = QLineEdit(self)
        self.rotor_position.setPlaceholderText("Enter rotor (e.g., 1,1,1)")
        self.rotor_position.setFixedSize(800, 50)
        self.rotor_position.setStyleSheet(self.input_style())
        input_layout.addWidget(self.rotor_position)

        self.plugboard_settings = QLineEdit(self)
        self.plugboard_settings.setPlaceholderText("Enter plugboard settings (e.g., AB CD EF)")
        self.plugboard_settings.setFixedSize(800, 50)
        self.plugboard_settings.setStyleSheet(self.input_style())
        input_layout.addWidget(self.plugboard_settings)

        button_layout = QHBoxLayout()

        self.encrypt_button = QPushButton("Encrypt", self)
        self.encrypt_button.setFixedSize(200, 60)
        self.encrypt_button.setStyleSheet(self.button_style())
        self.encrypt_button.clicked.connect(self.encrypt_message)
        button_layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton("Decrypt", self)
        self.decrypt_button.setFixedSize(200, 60)
        self.decrypt_button.setStyleSheet(self.button_style())
        self.decrypt_button.clicked.connect(self.decrypt_message)
        button_layout.addWidget(self.decrypt_button)

        input_layout.addLayout(button_layout)
        main_layout.addLayout(input_layout)

        self.output_message = QLabel(self)
        self.output_message.setFont(QFont("Courier", 16))
        self.output_message.setStyleSheet(self.label_style())
        main_layout.addWidget(self.output_message)

        self.letter_display = QTextEdit(self)
        self.letter_display.setFont(QFont("Courier", 20))
        self.letter_display.setStyleSheet("background-color: black; color: white; border: 2px solid #FFD700; padding: 10px;")
        self.letter_display.setReadOnly(True)
        self.letter_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.letter_display)

        central_widget.setLayout(main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)

    def input_style(self):
        return """
        QLineEdit {
            background-color: #1E1E1E;
            color: #00FF00;
            border: 2px solid #FFD700;
            padding: 5px;
            font-size: 24px;
        }
        QLineEdit:focus {
            border: 2px solid #00FF00;
        }
        """

    def button_style(self):
        return """
        QPushButton {
            background-color: #333333;
            color: #FFD700;
            border: 2px solid #FFD700;
            padding: 10px;
            font-size: 24px;
        }
        QPushButton:hover {
            background-color: #444444;
        }
        QPushButton:pressed {
            background-color: #555555;
            border: 2px solid #00FF00;
        }
        """

    def label_style(self):
        return """
        QLabel {
            color: #FFD700;
            background-color: #1E1E1E;
            padding: 10px;
            border: 2px solid #FFD700;
        }
        """

    def validate_inputs(self):
        try:
            rotor_pos = tuple(map(int, self.rotor_position.text().split(',')))
            if len(rotor_pos) != 3 or not all(1 <= pos <= 26 for pos in rotor_pos):
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Invalid rotor positions. Enter three numbers between 1 and 26.")
            return False

        plugboard = self.plugboard_settings.text().replace(" ", "").upper()
        if len(plugboard) % 2 != 0 or any(char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for char in plugboard):
            QMessageBox.critical(self, "Input Error", "Invalid plugboard settings. Ensure pairs are valid and characters are uppercase letters.")
            return False

        return True

    def encrypt_message(self):
        if not self.validate_inputs():
            return

        self.message = self.input_message.text().upper()
        self.rotor_pos = tuple(map(int, self.rotor_position.text().split(',')))
        self.plugboard = self.plugboard_settings.text().replace(" ", "").upper()

        self.processed_message = enigma(self.message, self.rotor_pos, plugb=self.plugboard)
        self.output_message.setText(f"Encrypted: {self.processed_message}")
        self.letter_display.clear()
        self.current_index = 0
        self.timer.start(100)  # Update every 100 ms

    def decrypt_message(self):
        if not self.validate_inputs():
            return

        self.message = self.input_message.text().upper()
        self.rotor_pos = tuple(map(int, self.rotor_position.text().split(',')))
        self.plugboard = self.plugboard_settings.text().replace(" ", "").upper()

        self.processed_message = enigma(self.message, self.rotor_pos, plugb=self.plugboard)
        self.output_message.setText(f"Decrypted: {self.processed_message}")
        self.letter_display.clear()
        self.current_index = 0
        self.timer.start(100)  # Update every 100 ms

    def update_display(self):
        if self.current_index < len(self.message):
            original_char = self.message[self.current_index]
            processed_char = self.processed_message[self.current_index]
            display_text = f"{original_char} -> {processed_char}\n"
            self.letter_display.append(display_text)

            if original_char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                self.letter_display.setTextColor(QColor('yellow'))
            else:
                self.letter_display.setTextColor(QColor('white'))

            self.current_index += 1
        else:
            self.timer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EnigmaApp()
    ex.show()
    sys.exit(app.exec_())

