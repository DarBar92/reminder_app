from PyQt6.QtWidgets import (
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHeaderView,  # Add this import
)

class RemindersTable(QWidget):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Name", "Frequency", "Sound Type"])

        # Make columns stretch to fill the available space
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_reminders(self, reminders_list):
        self.clear()
        for row_index, (name, frequency_str, sound) in enumerate(reminders_list):
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, QTableWidgetItem(name))
            self.table.setItem(row_index, 1, QTableWidgetItem(frequency_str))
            self.table.setItem(row_index, 2, QTableWidgetItem(sound))

    def get_selected_reminder(self):
        row= self.table.currentRow()
        if row == -1:
            return None
        name = self.table.item(row, 0).text()
        frequency_str = self.table.item(row, 1).text()
        sound = self.table.item(row, 2).text()
        return (name, frequency_str, sound)
    
    def clear(self):
        self.table.setRowCount(0)