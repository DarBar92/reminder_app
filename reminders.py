from PyQt6.QtWidgets import (
QMainWindow, 
QPushButton, 
QHBoxLayout,
QVBoxLayout, 
QWidget,
QLabel,
)
from add_reminder_dialog import AddReminderDialog
from reminders_table import RemindersTable
from notification_manager import NotificationManager
import csv

class Reminder(QMainWindow):
    CSV_FILE = "reminders.csv"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reminder App")
        self.setGeometry(100, 100, 600, 400)

        self.notification_manager = NotificationManager()

        self.setup_ui()
        self.load_reminders()
        
    def setup_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("There are no reminders set. Please click the button to set a reminder.")
        layout.addWidget(self.label)

        self.reminders_table = RemindersTable()
        layout.addWidget(self.reminders_table)

        button_layout = QHBoxLayout()
        self.add_reminder_button = self.create_button("Add Reminder", self.add_reminder)
        self.edit_reminder_button = self.create_button("Edit Reminder", self.edit_reminder)
        self.remove_reminder_button = self.create_button("Remove Reminder", self.remove_reminder)

        for button in (self.add_reminder_button, self.edit_reminder_button, self.remove_reminder_button):
            button_layout.addWidget(button)

        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_button(self, text, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        return button

    def add_reminder(self):
        dialog = AddReminderDialog()
        if dialog.exec():
            name = dialog.name_input.text()
            frequency = dialog.frequency_input.text()
            frequency_type = dialog.frequency_input_type.currentText()
            sound_type = dialog.sound_type_input.currentText()

            self.save_reminder(name, frequency, frequency_type, sound_type) 
            self.notification_manager.schedule_notification(name, frequency, frequency_type, sound_type)
            self.load_reminders()

    def save_reminder(self, name, frequency, frequency_type, sound_type):
        with open(self.CSV_FILE, "a") as file:
            file.write(f"{name},{frequency} {frequency_type},{sound_type}\n")

    
    def load_reminders(self):
        reminders = []
        try:
            with open(self.CSV_FILE, "r") as file:
                for line in file:
                    name, freq_str, sound = line.strip().split(",")
                    reminders.append((name, freq_str, sound))
        except FileNotFoundError:
            reminders = []

        if reminders:
            self.label.hide()
            self.reminders_table.show()
            self.reminders_table.load_reminders(reminders)

            for name, freq_str, sound in reminders:
                try:
                    frequency, frequency_type = freq_str.split()
                    self.notification_manager.schedule_notification(name, frequency, frequency_type, sound)
                except ValueError:
                    print(f"Skipping malformed reminder: {name}, {freq_str}, {sound}")
        else:
            self.label.show()
            self.reminders_table.hide()
            
    
    def remove_reminder(self):
        selected_row = self.reminders_table.table.currentRow()
        if selected_row == -1:
            print("No reminder selected.")
            return

        name = self.reminders_table.table.item(selected_row, 0).text()
        freq = self.reminders_table.table.item(selected_row, 1).text()
        sound = self.reminders_table.table.item(selected_row, 2).text()

        target_row = [name, freq, sound] 

        try:
            with open(self.CSV_FILE, "r", newline="") as file:
                reader = csv.reader(file)
                rows = list(reader)

            updated_rows = [row for row in rows if row != target_row]
            
            with open(self.CSV_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)

            self.notification_manager.stop_reminder(name)
            print(f"Removed reminder: {name}")
            self.load_reminders()

        except FileNotFoundError:
            print(f"{self.CSV_FILE} not found")
    
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

        dialog = AddReminderDialog()
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
                updated_rows = []
                with open(self.CSV_FILE, "r", newline="") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row == [old_name, f"{old_frequency} {old_freq_type}", old_sound]:
                            updated_rows.append([new_name, f"{new_frequency} {new_freq_type}", new_sound_type])
                        else:
                            updated_rows.append(row)

                with open(self.CSV_FILE, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerows(updated_rows)

            except FileNotFoundError:
                print("CSV file not found during edit.")
                return

            self.notification_manager.stop_reminder(old_name)
            self.notification_manager.schedule_notification(new_name, new_frequency, new_freq_type, new_sound_type)
            self.load_reminders()

    def closeEvent(self, event):
        self.notification_manager.stop_all()
        event.accept()