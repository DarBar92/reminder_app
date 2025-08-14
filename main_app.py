from PyQt6.QtWidgets import (
QMainWindow, 
QPushButton, 
QHBoxLayout,
QVBoxLayout, 
QWidget,
QLabel,
QTableWidgetItem,
)
from PyQt6.QtCore import QTime
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

        button_layout = QHBoxLayout()

        self.add_reminder_button = QPushButton("Add Reminder")
        self.add_reminder_button.clicked.connect(self.add_reminder)
        button_layout.addWidget(self.add_reminder_button)

        self.edit_reminder_button = QPushButton("Edit Reminder")
        self.edit_reminder_button.clicked.connect(self.edit_reminder)
        button_layout.addWidget(self.edit_reminder_button)
        
        self.remove_reminder_button = QPushButton("Remove Reminder")
        self.remove_reminder_button.clicked.connect(self.remove_reminder)
        button_layout.addWidget(self.remove_reminder_button)
        
        layout.addLayout(button_layout)

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
            sound_type = dialog.sound_type_input.currentText()

            self.save_reminder(name, frequency, frequency_type, sound_type) 
            self.notification_manager.schedule_notification(name, frequency, frequency_type, sound_type)
            self.load_reminders()

    def save_reminder(self, name, frequency, frequency_type, sound_type):
        with open("reminders.csv", "a") as file:
            file.write(f"{name},{frequency} {frequency_type},{sound_type}\n")

    
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

                        name = columns[0]
                        freq_and_type = columns[1].split()
                        frequency = freq_and_type[0]
                        frequency_type = freq_and_type[1]
                        sound = columns[2]

                        self.notification_manager.schedule_notification(name, frequency, frequency_type, sound)
                else:
                    self.label.show()
                    self.reminders_table.hide()
        except FileNotFoundError:
            self.label.show()
            self.reminders_table.hide()
    
    def remove_reminder(self):
        selected_row = self.reminders_table.table.currentRow()
        if selected_row == -1:
            print("No reminder selected.")
            return

        name_item = self.reminders_table.table.item(selected_row, 0)
        freq_item = self.reminders_table.table.item(selected_row, 1)
        sound_item = self.reminders_table.table.item(selected_row, 2)

        if not name_item:
            return
        
        reminder_name = name_item.text()
        reminder_freq = freq_item.text()
        reminder_sound = sound_item.text()

        target_line = f"{reminder_name},{reminder_freq},{reminder_sound}\n"

        try:
            with open("reminders.csv", "r") as file:
                lines = file.readlines()

            with open("reminders.csv", "w") as file:
                for line in lines:
                    if line.strip() != target_line.strip():
                        file.write(line)
            self.notification_manager.stop_reminder(reminder_name)

            print(f"Removed reminder: {reminder_name}")
            self.load_reminders()

        except FileNotFoundError:
            print("reminders.csv not found")
    
    def edit_reminder(self):
        selected_row = self.reminders_table.table.currentRow()
        if selected_row == -1:
            print("No reminder selected")
            return

        name_item = self.reminders_table.table.item(selected_row, 0)
        freq_item = self.reminders_table.table.item(selected_row, 1)
        sound_item = self.reminders_table.table.item(selected_row, 2)

        if not (name_item and freq_item and sound_item):
            print("Invalid selection")
            return
        
        old_name = name_item.text()
        old_frequency, old_freq_type = freq_item.text().split()
        old_sound = sound_item.text()

        dialog = Add_reminder_dialog()
        dialog.name_input.setText(old_name)
        dialog.frequency_input.setText(old_frequency)
        dialog.frequency_input_type.setCurrentText(old_freq_type)
        dialog.sound_type_input.setCurrentText(old_sound)

        if dialog.exec():
            new_name = dialog.name_input.text()
            new_frequency = dialog.frequency_input.text()
            new_freq_type = dialog.frequency_input_type.currentText()
            new_sound_type = dialog.sound_type_input.currentText()

            try:
                with open("reminders.csv", "r") as file:
                    lines = file.readlines()

                with open("reminders.csv", "w") as file:
                    for line in lines:
                        if line.strip() == f"{old_name},{old_frequency} {old_freq_type},{old_sound}":
                            file.write(f"{new_name},{new_frequency} {new_freq_type},{new_sound_type}")
                        else:
                            file.write(line)
            except FileNotFoundError:
                print("CSV file not found during edit.")
                return

            self.notification_manager.stop_reminder(old_name)
            self.notification_manager.schedule_notification(new_name, new_frequency, new_freq_type, new_sound_type)

            self.load_reminders()



    def closeEvent(self, event):
        if hasattr(self, 'notification_manager'):
            self.notification_manager.stop_all()
        event.accept()