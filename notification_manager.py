from PyQt6.QtWidgets import QSystemTrayIcon 
from PyQt6.QtGui import QIcon 
from PyQt6.QtCore import QDateTime, QTimer, QUrl
from PyQt6.QtMultimedia import QSoundEffect

class NotificationManager:
    def __init__(self):
        self.timers = {} 
        self.tray_icon = QSystemTrayIcon(QIcon("Assets/Timer.png"))  # Use a valid icon path
        self.tray_icon.setVisible(True)

        self.sounds = []

    def schedule_notification(self, name, frequency, frequency_type, sound):
        # Same timing logic as before...
        freq_map = {
            "Seconds": 1000,
            "Minutes": 60000,
            "Hours": 3600000
        }
        interval_ms = int(frequency) * freq_map[frequency_type]

        def display_notification():
            self.tray_icon.showMessage(
                f"Reminder: {name}",
                "It's time for your scheduled reminder!",
                QSystemTrayIcon.MessageIcon.Information,
                5000
            )
        
        def play_sound(sound_name):
            sound = QSoundEffect()
            sound.setVolume(0.5)

            if sound_name == "Posture":
                sound.setSource(QUrl.fromLocalFile("sounds/Posture.wav"))
            elif sound_name == "Hydrate":
                sound.setSource(QUrl.fromLocalFile("sounds/Hydrate.wav"))
            elif sound_name == "Beep":
                sound.setSource(QUrl.fromLocalFile("sounds/Beep.wav"))
            else:
                print(f"Unkown sound: {sound_name}")
            
            sound.play()
            self.sounds.append(sound)

            QTimer.singleShot(5000, lambda: self.sounds.remove(sound))

        if name in self.timers:
            self.timers[name].stop()
            del self.timers[name]

        periodic_timer = QTimer()
        periodic_timer.timeout.connect(lambda: [display_notification(), play_sound(sound)])
        periodic_timer.start(interval_ms)

        self.timers[name] = periodic_timer

    def stop_all(self):
        for timer in self.timers.values():
            timer.stop()
        self.timers.clear()
        print("All timers stopped.")
        self.sounds.clear()
        if self.tray_icon:
            self.tray_icon.hide()
            self.tray_icon.deleteLater()
            self.tray_icon = None
            print("Tray icon removed.")
    
    def stop_reminder(self, name):
        if name in self.timers:
            self.timers[name].stop()
            del self.timers[name]
            print(f"Timer for '{name}' stopped")

