from PyQt6.QtWidgets import (
    QWidget,
    QTableWidget,
    QVBoxLayout,
    QHeaderView,  # Add this import
)

class RemindersTable(QWidget):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Frequency", "Start Time", "Sound Type"])

        # Make columns stretch to fill the available space
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)