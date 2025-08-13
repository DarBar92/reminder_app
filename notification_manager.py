from PyQt6.QtWidgets import QSystemTrayIcon 
from PyQt6.QtGui import QIcon 
from PyQt6.QtCore import QDateTime, QTimer, QUrl
from PyQt6.QtMultimedia import QSoundEffect

class NotificationManager:
    def __init__(self):
        self.timers = []
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"))  # Use a valid icon path
        self.tray_icon.setVisible(True)

    def schedule_notification(self, name, frequency, frequency_type, start_time, sound):
        # Same timing logic as before...
        freq_map = {
            "Seconds": 1000,
            "Minutes": 60000,
            "Hours": 3600000
        }
        interval_ms = int(frequency) * freq_map[frequency_type]

        now = QDateTime.currentDateTime()
        start = QDateTime(now.date(), start_time)
        if start < now:
            start = start.addDays(1)
        delay_ms = now.msecsTo(start)

        def display_notification():
            self.tray_icon.showMessage(
                f"Reminder: {name}",
                "It's time for your scheduled reminder!",
                QSystemTrayIcon.MessageIcon.Information,
                5000
            )
        
        def play_sound(sound):
            self.sound = QSoundEffect()
            self.sound.setVolume(0.5)
            if sound == "Posture":
                self.sound.setSource(QUrl.fromLocalFile("sounds/Posture.mp3"))
            elif sound == "Hydrate":
                self.sound.setSource(QUrl.fromLocalFile("sounds/Hydrate.mp3"))
            elif sound == "Beep":
                self.sound.setSource(QUrl.fromLocalFile("sounds/Beep.mp3"))


        periodic_timer = QTimer()
        periodic_timer.timeout.connect(display_notification)

        initial_timer = QTimer()
        initial_timer.setSingleShot(True)
        initial_timer.timeout.connect(lambda: [
            display_notification(),
            play_sound(sound),
            periodic_timer.start(interval_ms)
        ])
        initial_timer.start(delay_ms)

        self.timers.append(initial_timer)
        self.timers.append(periodic_timer)

    def stop_all(self):
        for timer in self.timers:
            timer.stop()
        self.timers.clear()
        print("All timers stopped.")

        if self.tray_icon:
            self.tray_icon.hide()
            self.tray_icon.deleteLater()
            self.tray_icon = None
            print("Tray icon removed.")

