from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve, QPoint, Qt, QObject, QRunnable, QThreadPool, QTimer, pyqtSignal
from PyQt5.QtGui import QWindow, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QProgressBar, QListWidget, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect, QTextEdit, QStyle
from PyQt5 import QtCore
import sys
from custom_stacked_widget import QCustomQStackedWidget
import time

STYLESHEET = {} 
STYLESHEET["CustomFrame"]  = """
    QFrame {border-style: groove;
            border-width: 3px;
            background-color: #B2BABB;
            border-color: #2F4F4F;
            border-radius: 8px;
    }
"""

STYLESHEET["CustomFrame_inner"]  = """
    QFrame {border-style: groove;
            border-width: 1px;
            background-color: #F5EEF8;
            border-color: #2F4F4F;
            border-radius: 4px;
    }
"""

STYLESHEET["StatusView"] = """
    QFrame {border-style: groove;
                border-width: 1px;
                background-color: #F5EEF8;
                border-color: #2F4F4F;
                border-radius: 4px;
        }
    QLabel {
        border: None
    }
    QTextEdit{
        border-width: 0.5px;
        background-color: #212F3D;
        border-color: #2F4F4F;
        border-radius: 2px;
        color: #F5EEF8;
    } 
"""

class WorkerSignals(QObject):
    """
        Defines the signals available from a running worker thread.
        Supported signals are:
        finished
        No data
        error
        `str` Exception string
        result
        `dict` data returned from processing
    """
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(dict)
    step_finished = pyqtSignal()

class Worker(QRunnable):
    """
        Worker thread
        :param args: Arguments to make available to the run code
        :param kwargs: Keywords arguments to make available to the run
        :code
        :
    """
    def __init__(self, steps=5):
        super().__init__()
        self.signals = WorkerSignals() # Create an instance of our signals class.
        self._steps = steps

    def run(self):
        """
            Initialize the runner function with passed self.args,
            self.kwargs.
        """
        try:
            for step in range(self._steps):
                time.sleep(3)
                self.signals.step_finished.emit()
        except Exception as e:
            self.signals.error.emit(str(e))
        else:
            self.signals.finished.emit()
            self.signals.result.emit({"n": 0, "value": 0})

class CustomProcessButton(QPushButton):
    def __init__(self, parent=None, title_text = "Default"):
        super().__init__(parent)

        # self.setMinimumSize(60, 60)
        self.setText(title_text)

        self.color1 = QColor(26, 82, 118)
        self.color2 = QColor(169, 204, 227)

        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=250
        )

    def _animate(self, value):
        # qss = """
        #     font: 75 10pt "Microsoft YaHei UI";
        #     font-weight: bold;
        #     color: rgb(255, 255, 255);
        #     border-style: solid;
        #     border-radius:21px;
        # """
        qss = """
            border-style: solid;
            border-radius:4px;
        """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=self.color1.name(), color2=self.color2.name(), value=value
        )
        qss += grad
        self.setStyleSheet(qss)

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)

class StatusView(QWidget):
    def __init__(self, parent=None, process_name:str = "process", process_id:int=0):

        # -- Call inherited constructor
        super(StatusView, self).__init__(parent)

        self._process_name = process_name
        self._process_id = process_id

        self._configure_window()
        self._create_content()
        self.setStyleSheet(STYLESHEET["StatusView"])

    def _configure_window(self):
        pass 

    def _create_content(self):

        # -- Create main layout
        self.window_vlayout = QVBoxLayout()

        # -- Create widgets
        self.process_name_label = QLabel(f"{self._process_name} (id = {self._process_id})")
        self.central_frame = QFrame()
        # self.central_frame.setStyleSheet(STYLESHEET["CustomFrame_inner"])
        self.progress_bar = QProgressBar()

        effect = QGraphicsDropShadowEffect(
            offset=QPoint(3, 3), blurRadius=10, color=QColor("#2F4F4F")
        )
        self.central_frame.setGraphicsEffect(effect)

        # -- Add widgets to layout
        self.window_vlayout.addWidget(self.process_name_label)
        self.window_vlayout.addWidget(self.central_frame)
        self.window_vlayout.addWidget(self.progress_bar)

        self.setLayout(self.window_vlayout)

        # --- CENTRAL FRAME --- 
        # -- Create content inside central_frame
        self._central_frame_layout = QVBoxLayout()

        # -- Create widgets
        self._text_edit = QTextEdit()
        # -- Add widgets to layout
        self._central_frame_layout.addWidget(self._text_edit)
        # -- Set layout to central frame
        self.central_frame.setLayout(self._central_frame_layout)


        # -- Resize 
        self.resize_widgets_in_layout()

    def resize_widgets_in_layout(self):

        self.window_vlayout.setStretch(0, 1)
        self.window_vlayout.setStretch(1, 10)
        self.window_vlayout.setStretch(2, 1)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        # -- Call inherited constructor
        super(MainWindow, self).__init__(parent)
        self._n_process_executed = 0
        self.show_process_btn_list = []
        self._status_view_list = []

        self._configure_window()
        self._create_content()

    def _configure_window(self):
        # -- Configure main window
        self.setWindowTitle("Customized widgets")
        self.setGeometry(100, 100, 800, 600)  # (x, y, width, height)

    def _create_content(self):
        # -- Create Central widget for main window
        self.main_central_widget = QWidget()
        self.setCentralWidget(self.main_central_widget)

        # -- Create main layout
        self.main_window_vlayout = QVBoxLayout()

        # -- Create widgets
        self.description_label = QLabel("Generate status processes")
        self.central_frame = QFrame()
        self.central_frame.setStyleSheet(STYLESHEET["CustomFrame"])
        self.run_btn = QPushButton("run")


        # -- Add widgets to layout
        self.main_window_vlayout.addWidget(self.description_label)
        self.main_window_vlayout.addWidget(self.central_frame)
        self.main_window_vlayout.addWidget(self.run_btn)

        # -- Set layout to main window
        self.main_central_widget.setLayout(self.main_window_vlayout)

        # -- Resize 
        self.resize_widgets_in_layout()

        # -- Create stacked status views
        self._create_process_status_section()

        # -- Connections
        self.run_btn.clicked.connect(self._run_process)

    def _run_process(self):
        self._n_process_executed += 1
        self._add_show_process_btn()
        self._resize_process_btns()

    def resize_widgets_in_layout(self):

        self.main_window_vlayout.setStretch(0, 1)
        self.main_window_vlayout.setStretch(1, 10)
        self.main_window_vlayout.setStretch(2, 1)

    def _resize_process_btns(self):
        for btn in self.show_process_btn_list:
            btn.resize(int(self.process_btn_widget.width() * 0.8), int(self.process_btn_widget.height() * 0.06))
            btn.setMinimumSize(int(self.process_btn_widget.width() * 0.8), int(self.process_btn_widget.height() * 0.06))

    def _create_process_status_section(self):

        # -- Create layout for main frame 
        self.central_frame_layout = QHBoxLayout()

        # -- Create widgets
        self.left_frame = QFrame()
        self.right_frame = QFrame()
        self.left_frame.setStyleSheet(STYLESHEET["CustomFrame_inner"])
        self.right_frame.setStyleSheet(STYLESHEET["CustomFrame_inner"])

        # -- Add widgets to layout
        self.central_frame_layout.addWidget(self.left_frame)
        self.central_frame_layout.addWidget(self.right_frame)

        # -- Resize widgets in layout
        self.central_frame_layout.setStretch(0, 1)
        self.central_frame_layout.setStretch(1, 3)

        # -- Set layout to frame
        self.central_frame.setLayout(self.central_frame_layout)

        # -- Create left section 
        self._create_left_btns_section()

        # -- Create right section
        self._create_right_log_section()

        # -- process btns connections
        # for btn_id, btn in enumerate(self.show_process_btn_list):
        #     # print("btn_id:", btn_id)
        #     btn.clicked.connect(lambda: self._show_status_view(btn_id))

    def _show_status_view(self, btn_id):
        # self._status_view_list[btn_id].show()
        self._status_stack.slideToWidget(self._status_view_list[btn_id])

    def _create_right_log_section(self):
        #  -- Create layout for left frame
        self.right_frame_layout = QVBoxLayout()

        # -- Create widgets
        # self._status_view_list = []
        # for process_i in range(self._n_process_executed):
        #     process_id_parsed = int(f"{process_i + 1}")
        #     # print(process_id_parsed)
        #     status_view = StatusView(process_id= process_id_parsed)
        #     self._status_view_list += [status_view]

        self._status_stack = QCustomQStackedWidget()
        self._status_stack.setTransitionSpeed(500)
        _style = """
        QStackedWidget{
            border: none
        } 
        """
        self._status_stack.setStyleSheet(_style)

        self._main_content_widget = QWidget()
        self._status_stack.addWidget(self._main_content_widget)
        # for status_view in self._status_view_list:
        #     self._status_stack.addWidget(status_view)

        self.right_frame_layout.addWidget(self._status_stack)

        self.right_frame.setLayout(self.right_frame_layout)
        


    def _create_left_btns_section(self):

        self.process_view_is_shown = False
        # -- Create layout for left frame
        self.left_frame_layout = QVBoxLayout()

        # -- Create widgets
        self.show_process_btn = QPushButton("Show status")
        self.process_btn_stack = QCustomQStackedWidget()
        self.process_btn_stack.setTransitionSpeed(500)
        _style = """
        QStackedWidget{
            border: none
        } 
        """
        self.process_btn_stack.setStyleSheet(_style)

        style = self.show_process_btn.style() # Get the QStyle object from the widget.
        icon = style.standardIcon(QStyle.SP_ArrowUp)
        self.show_process_btn.setIcon(icon)

        self.empty_widget = QWidget()
        self.process_btn_widget = QWidget()

        self._process_widget_layout = QVBoxLayout()
        for i in range(self._n_process_executed):
            show_btn = CustomProcessButton(title_text = f"Process {i + 1} (0%)")
            show_btn.clicked.connect(lambda ch, btn_id=i: self._show_status_view(btn_id))
            self.show_process_btn_list += [show_btn]
            
        vspacer_1 = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # vspacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self._process_widget_layout.addItem(vspacer_1)
        for btn in self.show_process_btn_list:
            self._process_widget_layout.addWidget(btn)
        # self._process_widget_layout.addItem(vspacer_2)
        


        self.process_btn_widget.setLayout(self._process_widget_layout)
        self.process_btn_stack.addWidget(self.empty_widget)
        self.process_btn_stack.addWidget(self.process_btn_widget)


        #-- Add widgets to layout
        self.left_frame_layout.addWidget(self.process_btn_stack)
        self.left_frame_layout.addWidget(self.show_process_btn)
        

        # -- Set layout to frame 
        self.left_frame.setLayout(self.left_frame_layout)

        # Connect btns
        self.show_process_btn.clicked.connect(self._show_status)

    def _add_show_process_btn(self):

        i = self._n_process_executed - 1
        show_btn = CustomProcessButton(title_text = f"Process {i + 1} (0%)")
        self.show_process_btn_list += [show_btn]
        self._process_widget_layout.addWidget(show_btn)

        # -- Create widgets
        process_id_parsed = int(f"{i + 1}")
        status_view = StatusView(process_id= process_id_parsed)
        self._status_view_list += [status_view]
        self._status_stack.addWidget(status_view)
        print("process:", i)

        show_btn.clicked.connect(lambda ch, btn_id=i: self._show_status_view(btn_id))


    def _show_status(self):

        # for process_btn in self.show_process_btn_list:
        #     if self.process_view_is_shown:
        #         process_btn.hide()
        #     else:
        #         process_btn.show()

        # if self.process_view_is_shown:
        #     self.process_view_is_shown = False
        # else:
        #     self.process_view_is_shown = True

        index = self.process_btn_stack.currentIndex()

        if index == 1:
            next_index = 0
        else:
            next_index = 1
        
        if next_index == 0:
            self.process_btn_stack.slideToWidget(self.empty_widget)
            self._status_stack.slideToWidgetIndex(0)

            style = self.show_process_btn.style() # Get the QStyle object from the widget.
            icon = style.standardIcon(QStyle.SP_ArrowUp)
            self.show_process_btn.setIcon(icon)
        elif next_index == 1:
            self.process_btn_stack.slideToWidget(self.process_btn_widget)
            self._status_stack.slideToWidgetIndex(1)
            style = self.show_process_btn.style() # Get the QStyle object from the widget.
            icon = style.standardIcon(QStyle.SP_ArrowDown)
            self.show_process_btn.setIcon(icon)

        self._resize_process_btns()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())