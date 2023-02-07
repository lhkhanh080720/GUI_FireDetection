from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget

# Default
app = QApplication([])

widget = QWidget()

# Vertical layout 
# Step1: Add into "layout"
# Step2: Set "layput" for "widget" and show "widget"
layout = QVBoxLayout()
label = QLabel("Hello World!")
layout.addWidget(label) # Step1

button = QPushButton("Click")
layout.addWidget(button) # Step1

widget.setLayout(layout) # Step2

widget.show()
# Default
app.exec_()