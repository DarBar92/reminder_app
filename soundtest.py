from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtWidgets import QApplication
import os
import sys

app = QApplication(sys.argv)

sound = QSoundEffect()
path = os.path.abspath("/home/darbar/Storage/Vscode Projects/Python/reminder_app/sounds/Beep.wav")
sound.setSource(QUrl.fromLocalFile(path))
sound.setVolume(0.5)

def try_play():
    if sound.status() == QSoundEffect.Status.Ready:
        print("✅ Sound is ready — playing.")
        sound.play()
        QTimer.singleShot(3000, app.quit)  # Allow 3 seconds for playback
    elif sound.status() == QSoundEffect.Status.Error:
        print("❌ Failed to load sound.")
        app.quit()
    else:
        print("🔄 Waiting for sound to load...")
        QTimer.singleShot(100, try_play)

print("Loading sound...")
try_play()
app.exec()
