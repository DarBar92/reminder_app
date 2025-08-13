from PyQt6.QtWidgets import (
QVBoxLayout, 
QHBoxLayout,
QFormLayout, 
QLineEdit,
QDialog,
QPushButton,
QComboBox,
QTimeEdit,
)
from PyQt6.QtGui import QIntValidator

class Add_reminder_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Reminder")
        self.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()
        # --- Form layout for input fields ---
        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        form_layout.addRow("Name:", self.name_input)
        frequency_input_layout = QHBoxLayout()
        self.frequency_input = QLineEdit()
        self.frequency_input.setValidator(QIntValidator())  # Ensure frequency is an integer
        self.frequency_input_type = QComboBox()
        self.frequency_input_type.addItems(["Seconds", "Minutes", "Hours"])
        form_layout.addRow("Frequency:", frequency_input_layout)
        frequency_input_layout.addWidget(self.frequency_input)
        frequency_input_layout.addWidget(self.frequency_input_type)
        self.start_time_input = QTimeEdit()
        form_layout.addRow("Start Time:", self.start_time_input)
        self.sound_type_input = QComboBox()
        self.sound_type_input.addItems(["Posture", "Hydrate", "Beep"])
        form_layout.addRow("Sound Type:", self.sound_type_input)

        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)