from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QMainWindow

# Default
app = QApplication([])

window = QMainWindow()

# Add into "window"
label = QLabel(parent=window, text="Hello World!")
label.move()

button = QPushButton(parent=window, text="Click")

# Show window
window.show()
# Default
app.exec_()