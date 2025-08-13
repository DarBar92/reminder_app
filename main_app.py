from PyQt6.QtWidgets import (
QMainWindow, 
QPushButton, 
QVBoxLayout, 
QWidget,
QLabel,
QTableWidgetItem,
)
from add_reminder_dialog import Add_reminder_dialog
from reminders_table import RemindersTable
from notification_manager import NotificationManager

class Reminder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reminder App")
        self.setGeometry(100, 100, 600, 400)

        self.notification_manager = NotificationManager()

        layout = QVBoxLayout()

        self.label = QLabel("There are no reminders set. Please click the button to set a reminder.")
        layout.addWidget(self.label)

        self.reminders_table = RemindersTable()
        layout.addWidget(self.reminders_table)
        
        self.add_reminder_button = QPushButton("Add Reminder")
        self.add_reminder_button.clicked.connect(self.add_reminder)
        layout.addWidget(self.add_reminder_button)
        

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.load_reminders()

    def add_reminder(self):
        dialog = Add_reminder_dialog()
        if dialog.exec():
            name = dialog.name_input.text()
            frequency = dialog.frequency_input.text()
            frequency_type = dialog.frequency_input_type.currentText()
            start_time = dialog.start_time_input.time()
            sound_type = dialog.sound_type_input.currentText()
            self.save_reminder(name, frequency, frequency_type, start_time.toString("HH:mm:ss"), sound_type) 
            self.notification_manager.schedule_notification(name, frequency, frequency_type, start_time, sound_type)
            self.load_reminders()

    def save_reminder(self, name, frequency, frequency_type, start_time, sound_type):
        with open("reminders.csv", "a") as file:
            file.write(f"{name},{frequency} {frequency_type},{start_time},{sound_type}\n")

    
    def load_reminders(self):
        try:
            with open("reminders.csv", "r") as file:
                reminders = [line.strip() for line in file.readlines()]
                if reminders:
                    self.label.hide()
                    self.reminders_table.show()
                    self.reminders_table.table.setRowCount(0)  # Clear existing rows
                    for row_index, row_data in enumerate(reminders):
                        columns = row_data.split(",")
                        self.reminders_table.table.insertRow(row_index)
                        for col, item in enumerate(columns):
                            self.reminders_table.table.setItem(row_index, col, QTableWidgetItem(item))
                else:
                    self.label.show()
                    self.reminders_table.hide()
        except FileNotFoundError:
            self.label.show()
            self.reminders_table.hide()
    
    def closeEvent(self, event):
        if hasattr(self, 'notification_manager'):
            self.notification_manager.stop_all()
        event.accept()