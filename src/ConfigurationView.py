from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, 
    QWidget, QMainWindow, 
    QFrame, QPushButton, QTextEdit
) 
from PyQt5.QtCore import pyqtSignal

class MissionConfigurationview(QWidget):
    creation_event_signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        print("MissionConfigurationview")
        self.setWindowTitle("Mission Configuration")
        self.setGeometry(300, 300, 500, 500)

        self._main_layout = QVBoxLayout()

        # -- couple label + text edit
        self._fields = ["name", "img", "launch_date", "cost", "mission_type", "comments"]
        self._values_set = {}
        for field in self._fields:
            field_widget = QWidget()
            layout = QVBoxLayout()

            tag_label = QLabel(field)
            text_edit = QTextEdit()
            text_edit.setFixedHeight(30)
            self._values_set[field] = text_edit

            layout.addWidget(tag_label)
            layout.addWidget(text_edit)
            field_widget.setLayout(layout)

            self._main_layout.addWidget(field_widget)

        self._create_btn = QPushButton("Create")
        self._create_btn.clicked.connect(self.dispatch_creation_event)
        self._main_layout.addWidget(self._create_btn)


        self.setLayout(self._main_layout)

    def dispatch_creation_event(self):
        print("dispatch_creation_event")
        object_dict = dict()
        for field in self._fields:
            object_dict[field] = self._values_set[field].toPlainText()
        
        self.creation_event_signal.emit(object_dict)


