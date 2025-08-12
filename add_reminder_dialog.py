from PyQt6.QtWidgets import (
QVBoxLayout, 
QHBoxLayout,
QFormLayout, 
QLineEdit,
QDialog,
QPushButton
)
class Add_reminder_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Reminder")
        self.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()
        # --- Form layout for input fields ---
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.frequency_input = QLineEdit()
        self.start_time_input = QLineEdit()
        self.end_time_input = QLineEdit()

        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Frequency:", self.frequency_input)
        form_layout.addRow("Start Time:", self.start_time_input)
        form_layout.addRow("End Time:", self.end_time_input)

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