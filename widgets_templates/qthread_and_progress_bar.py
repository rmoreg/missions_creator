import sys
from time import sleep
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QProgressBar, QVBoxLayout, QFrame, QPushButton, QDockWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QVariantAnimation, QSequentialAnimationGroup, QPropertyAnimation, QEasingCurve, QRect, QTimer, QAbstractAnimation
from PyQt5.QtGui import QColor

STYLESHEET = {} 
STYLESHEET["CustomFrame"]  = """
    QFrame {border-style: groove;
            border-width: 3px;
            background-color: #F0FFFF;
            border-radius: 2px;
            border-color: #2F4F4F;
    }
"""

STYLESHEET["CustomDock"]  = """
    QDockWidget {border-style: groove;
                border-width: 1px;
                background-color: #F0FFFF;
                border-radius: 2px;
                border-color: #2F4F4F;
    }
    QDockWidget::title {
        border-style: groove;
        border-width: 2px;
        border-radius: 1px;
        text-align: left; /* align the text to the left */
        background: #00CED1;
        padding-left: 5px;
    }

    QDockWidget::close-button, QDockWidget::float-button {
        border: 1px solid transparent;
        background: #BDB76B;
        padding: 0px;
    }

    QDockWidget::close-button:hover, QDockWidget::float-button:hover {
        background: gray;
    }

    QDockWidget::close-button:pressed, QDockWidget::float-button:pressed {
        padding: 1px -1px -1px 1px;
    }
"""

STYLESHEET["ProgressBar"]  = """
    QProgressBar {
        border: 2px solid grey;
        border-radius: 5px;
        text-align: center;
    }
"""

STYLESHEET["PushButton"]  = """
    QPushButton {
        background-color: #00CED1;
        border: 2px solid grey;
        border-radius: 5px;
        text-align: center;
    }

    QPushButton:hover{
        background-color: #BDB76B;
    } 
"""

class WorkerThread(QThread):
    update_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        print("running!")
        for thread_id in range(10):
            sleep(3)
            progress_value = int((100 * (thread_id + 1)) / (10))

            self.update_signal.emit(progress_value)

class GradientFrame(QFrame):
    def __init__(self):
        super().__init__()
        style = """
            QFrame 
                {
                    border: 2px solid red;
                }
        """
        self.setStyleSheet(style)

        self.animation = QPropertyAnimation(self, b"lineWidth")
        self.animation.setStartValue(2)
        self.animation.setEndValue(10)
        self.animation.setDuration(2000)
        self.animation.setLoopCount(-1)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

        self.animation.start()

    def getLineWidth(self):
        return self.property("lineWidth")

    def setLineWidth(self, width):
        print(width)
        style = f'QFrame {{border: {width}px solid red;}} '

        self.setStyle(style)
    
    lineWidth = property(getLineWidth, setLineWidth)
    



class GradientFrame_v2(QFrame):
    def __init__(self):
        super().__init__()
        self._increase = True
        self._decrease = False
        self._iter = 0
        self._n_cycle = 1

        style = """
            QFrame 
                {
                    border: 0px solid red;
                }
        """
        self.setStyleSheet(style)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_border)

        self.timer.start(1000)

    def animate_border(self):
        current_width = float(self.styleSheet().split(":")[1].split("px")[0])
        print("current_width:", current_width)

        # if current_width > 0 and current_width < 3:
        #     new_width = current_width + 0.1
        # elif current_width > 3:
        #     new_width = current_width - 0.1
        # else:
        #     new_width = current_width + 0.1
        # color = "black"

        if self._increase == True and current_width > 5:
            self._increase = False
            self._decrease = True
            
        elif self._decrease == True and current_width < 1:
            self._increase = True
            self._decrease = False
            
        if self._increase:
            new_width = current_width + 0.1
            if current_width >= 0 and current_width < (5/6):
                color = "#DAF7A6"
            elif current_width > (5/6) * 1 and current_width < (5/6) * 2:
                color = "#FFC300"
            elif current_width > (5/6) * 2 and current_width < (5/6) * 3:
                color = "#FF5733"
            elif current_width > (5/6) * 3 and current_width < (5/6) * 4:
                color = "#C70039"
            elif current_width > (5/6) * 4 and current_width < (5/6) * 5:
                color = "#900C3F"
            elif current_width > (5/6) * 5 and current_width < (5/6) * 6:
                color = "#581845"
        else:
            new_width = current_width - 0.1
            if current_width >= 0 and current_width < (5/6):
                color = "#DAF7A6"
            elif current_width > (5/6) * 1 and current_width < (5/6) * 2:
                color = "#FFC300"
            elif current_width > (5/6) * 2 and current_width < (5/6) * 3:
                color = "#FF5733"
            elif current_width > (5/6) * 3 and current_width < (5/6) * 4:
                color = "#C70039"
            elif current_width > (5/6) * 4 and current_width < (5/6) * 5:
                color = "#900C3F"
            elif current_width > (5/6) * 5:
                color = "#581845"

        
        color_palette = ["#DAF7A6", "#FFC300", "#FF5733", "#C70039", "#900C3F", "#581845"]
        print("iter:", self._iter)
        if self._n_cycle % 2 == 0:
            color = color_palette[-(self._iter + 1)]
        else:
            color = color_palette[self._iter]

        if self._iter % 2 == 0:
            width = 0
        else:
            width = 3
        
        # style = f'QFrame {{border: {new_width}px solid {color};}} '
        style = f'QFrame {{border: {width}px solid {color};}} '

        self.setStyleSheet(style)

        max_iter = 6
        if self._iter < max_iter - 1:
            self._iter = self._iter + 1
        else:
            self._iter = 0
            self._n_cycle += 1

class GradientFrame_v3(QFrame):
    def __init__(self):
        super().__init__()
        self.color1 = QColor(0, 0, 140, 255)
        # self.color2 = QColor(255, 255, 255, 255)
        self.color2 = QColor(170, 255, 255)

        self._animation_border = QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=10000
        )

        self._animation_background = QVariantAnimation(
            self,
            valueChanged=self._animate_background,
            startValue=0.00001,
            endValue=0.9999,
            duration=500
        )


        # style = """
        #     QFrame 
        #         {
        #             border: 5px solid;
        #             border-top-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0.1 rgba(0, 0, 140, 255), stop:0.9 rgba(255, 255, 255, 255));
        #             border-left-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(0, 0, 140, 255), stop:1 rgba(255, 255, 255, 255));
        #             border-bottom-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 140, 255), stop:1 rgba(255, 255, 255, 255));
        #             border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 140, 255), stop:1 rgba(255, 255, 255, 255));
        #         }
        # """
        # border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 140, 255), stop:1 rgba(255, 255, 255, 255));
        # border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.447368 rgba(0, 0, 255, 255), stop:1 rgba(255, 255, 255, 255));
        # border-top-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.495, fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(0, 0, 127, 255));

    def _animate(self, value):
        self._style = """
                border: 5px solid;
                border-radius: 15px;
                """

        
        grad = "border-top-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1}); border-bottom-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1}); border-left-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1}); border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1})".format(
            color1=self.color1.name(), color2=self.color2.name(), value=value
        )
        self._style += grad
        self.setStyleSheet(self._style)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_border)

        self.timer.start(10)

    def _animate_background(self, value):
        color_1 = QColor(208, 211, 212)
        color_2 = QColor(240, 243, 244)
        self._style = """
                border: 5px solid;
                border-radius: 15px;
                """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=color_1.name(), color2=color_2.name(), value=value
        )

        self._style += grad
        self.setStyleSheet(self._style)

    def animate_border(self):
        self._animation_border.setDirection(QAbstractAnimation.Forward)
        self._animation_border.start()


    def enterEvent(self, event):
        self._animation_background.setDirection(QAbstractAnimation.Forward)
        self._animation_background.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation_background.setDirection(QAbstractAnimation.Backward)
        self._animation_background.start()
        super().enterEvent(event)



class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        # -- Call inherited constructor
        super(MainWindow, self).__init__(parent)

        # -- Configure main window
        self.setWindowTitle("Threads")
        self.setGeometry(100, 100, 800, 600)  # (x, y, width, height)

        # -- Create Central widget for main window
        self.main_central_widget = QWidget()
        self.setCentralWidget(self.main_central_widget)

        # -- Create main layout
        self.main_window_vlayout = QVBoxLayout()


        # -- Create frames for main window sections
        self.top_frame = QFrame()
        self.top_frame.setStyleSheet(STYLESHEET["CustomFrame"])
        # self.central_frame = QFrame()
        # self.central_frame.setStyleSheet(STYLESHEET["CustomFrame"])
        self.central_frame = GradientFrame_v2()
        # self.bottom_frame = QFrame()
        # self.bottom_frame.setStyleSheet(STYLESHEET["CustomFrame"])
        self.bottom_frame = GradientFrame_v3()

        self._start_frames_gradient_animation()

        # -- Create progress bar
        self.global_progress_bar = QProgressBar()
        self.global_progress_bar.setMaximum(100)
        # self.global_progress_bar.setStyleSheet(STYLESHEET["ProgressBar"])
        self._start_progress_gradient_animation()

        # Create buttons
        self.threads_status_btn = QPushButton("Show threads status")
        self.threads_status_btn.setStyleSheet(STYLESHEET["PushButton"])
        self.run_btn = QPushButton("Run")

        # -- Add widgets to layout
        self.main_window_vlayout.addWidget(self.top_frame)
        self.main_window_vlayout.addWidget(self.central_frame)
        self.main_window_vlayout.addWidget(self.bottom_frame)
        self.main_window_vlayout.addWidget(self.global_progress_bar)
        self.main_window_vlayout.addWidget(self.threads_status_btn)
        self.main_window_vlayout.addWidget(self.run_btn)

        # -- Set layout to main window
        self.main_central_widget.setLayout(self.main_window_vlayout)


        # -- Add functionality to button
        self.threads_status_shown = True
        self.threads_status_btn.clicked.connect(self._show_threads_status)
        self.run_btn.clicked.connect(self._run_process)

        # --- Create dock widget 
        self.thread_status_dock = QDockWidget('Threads status', self)
        self.thread_status_dock.setStyleSheet(STYLESHEET["CustomDock"])
        self.thread_status_dock.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.thread_status_dock)
        self.thread_status_dock.setMinimumWidth(self.width() * (1/4))
        # self.thread_status_dock.hide()


    def _show_threads_status(self):
        print("Show threads status")
        current_width = self.thread_status_dock.width()
        print("current_width", current_width)
        

        if not self.threads_status_shown:
            # self.thread_status_dock.show()
            self.threads_status_shown = True
            extension = self.width() * (1/4)

        else:
            # self.thread_status_dock.hide()
            self.threads_status_shown = False
            extension = 0

        self.status_dock_animation = QPropertyAnimation(self.thread_status_dock, b"minimumWidth")
        self.status_dock_animation.setStartValue(current_width)
        self.status_dock_animation.setEndValue(extension)
        self.status_dock_animation.setDuration(1000)
        self.status_dock_animation.setEasingCurve(QEasingCurve.InSine)
        self.status_dock_animation.start()

        # Show message box
        # msg = QMessageBox()
        # msg.setWindowTitle("Warning")
        # msg.exec_()



    def _run_process(self):
        N_PARALLEL = 10

        # -- Configure dock section
        self.thread_status_layout = QVBoxLayout()
        self.status_widget = QWidget()
        self.status_label_1 = QLabel("Label 1")
        self.status_label_2 = QLabel("Label 2")
        self.thread_status_layout.addWidget(self.status_label_1)
        self.thread_status_layout.addWidget(self.status_label_2)
        self.status_widget.setLayout(self.thread_status_layout)

        self.thread_status_dock.setWidget(self.status_widget)
        
        
        self.worker = WorkerThread()
        self.worker.update_signal.connect(self._update_progress)
        self.worker.start()

    def _update_progress(self, progress_value:int):
        self.global_progress_bar.setValue(progress_value)

    def _start_progress_gradient_animation(self):

        _animation_fw = QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.0001,
            endValue=0.9999,
            duration=5000,
        )
        _animation_bw = QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.9999,
            endValue=0.0001,
            duration=5000,
        )
        self._group_animation = QSequentialAnimationGroup(self)
        self._group_animation.addAnimation(_animation_fw)
        self._group_animation.addAnimation(_animation_bw)
        self._group_animation.setLoopCount(-1)
        self._group_animation.start()

    def _start_frames_gradient_animation(self):
        _animation_fw = QVariantAnimation(
            self,
            valueChanged=self._animate_2,
            startValue=0.0001,
            endValue=0.9999,
            duration=5000,
        )
        _animation_bw = QVariantAnimation(
            self,
            valueChanged=self._animate_2,
            startValue=0.9999,
            endValue=0.0001,
            duration=5000,
        )
        self._group_animation_2 = QSequentialAnimationGroup(self)
        self._group_animation_2.addAnimation(_animation_fw)
        self._group_animation_2.addAnimation(_animation_bw)
        self._group_animation_2.setLoopCount(-1)
        self._group_animation_2.start()


    def _animate(self, value):
        animation_style = f"""
        QProgressBar::chunk {{
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF8C00, stop:{value} #FFF8DC, stop: 1.0 #FF8C00);
        }}"""


        gradient_style = STYLESHEET["ProgressBar"] + animation_style
        self.global_progress_bar.setStyleSheet(gradient_style)

    def _animate_2(self, value):
        animation_style = f"""
        QFrame::chunk {{
            border-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FF8C00, stop:{value} #FFF8DC, stop: 1.0 #FF8C00);
        }}"""


        gradient_style = STYLESHEET["CustomFrame"] + animation_style
        self.top_frame.setStyleSheet(gradient_style)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())