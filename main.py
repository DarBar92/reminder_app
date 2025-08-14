import sys
from reminders import Reminder
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Reminder()
    window.show()
    sys.exit(app.exec())