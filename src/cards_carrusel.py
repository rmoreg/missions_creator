import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QVBoxLayout, QWidget, QMainWindow, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtGui import QColor, QPainter, QTransform, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QPoint, pyqtSignal

from CardsContainerWidget import CardsContainerWidget

CARRUSEL = False
STYLESHEET = {}
STYLESHEET["CustomCardWidget"]  = """
    QWidget {border-style: solid;
            border-width: 2px;
            border-color: #2F4F4F;
            border-radius: 8px;
    }
"""

STYLESHEET["CustomCardWidget-clicked"]  = """
    QWidget {border-style: solid;
            border-width: 2.5px;
            border-color: white;
            border-radius: 8px;
    }
"""

STYLESHEET["CustomFrame"]  = """
    QFrame#customFrame {border-style: solid;
            border-width: 1px;
            border-color: #2F4F4F;
            border-radius: 4px;
            background-color: white;
    }
"""

class CardWidget(QWidget):
    card_selected_signal = pyqtSignal(str)
    def __init__(self, parent= None, title=None, img_path="") -> None:
        super().__init__(parent)
        self.title = title
        self.clicked_flag = False
        self.clicked_counter = 0
        self.img_path = img_path
        self.setStyleSheet(STYLESHEET["CustomCardWidget"])
        
        effect = QGraphicsDropShadowEffect(
            offset=QPoint(3, 3), blurRadius=10, color=QColor("#2F4F4F")
        )
        self.setGraphicsEffect(effect)

        STYLESHEET["CustomLabel"]  = """
            QLabel 
            {
                color: #2F4F4F;
                font-size: 16px;
            }
        """

        STYLESHEET["CustomLabel-clicked"]  = """
            QLabel 
            {
                color: white;
                font-size: 20px;
            }
        """
        self.label = QLabel(title, self)
        self.label.setStyleSheet(STYLESHEET["CustomLabel"])
        self.label.setAlignment(Qt.AlignTop)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.setFixedSize(300, 300)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(100)
        self.animation.setLoopCount(1)

    def enterEvent(self, event) -> None:
        if not self.clicked_flag:
            self.setCursor(Qt.PointingHandCursor)

            # self.animation.setStartValue(self.geometry())
            # self.animation.setEndValue(self.geometry().adjusted(-10, -10, 5, 5))
            # self.animation.start()

            effect = QGraphicsDropShadowEffect(
                offset=QPoint(15, 15), blurRadius=20, color=QColor("#2F4F4F")
            )
            self.setGraphicsEffect(effect)

    def restart_position(self):
        if self.clicked_flag:
            # self.animation.setStartValue(self.geometry())
            # self.animation.setEndValue(self.geometry().adjusted(10, 10, -5, -5))
            # self.animation.start()

            effect = QGraphicsDropShadowEffect(
                offset=QPoint(3, 3), blurRadius=10, color=QColor("#2F4F4F")
            )
            self.setGraphicsEffect(effect)

            self.label.setStyleSheet(STYLESHEET["CustomLabel"])
            self.setStyleSheet(STYLESHEET["CustomCardWidget"])

    def leaveEvent(self, event) -> None:
        if not self.clicked_flag:
            # self.animation.setStartValue(self.geometry())
            # self.animation.setEndValue(self.geometry().adjusted(10, 10, -5, -5))
            # self.animation.start()

            effect = QGraphicsDropShadowEffect(
                offset=QPoint(3, 3), blurRadius=10, color=QColor("#2F4F4F")
            )
            self.setGraphicsEffect(effect)
        else:
            pass

    def paintEvent(self, event) -> None:
        # painter = QPainter(self)
        # painter.setRenderHint(QPainter.Antialiasing)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing)
        
        # transform = QTransform()
        # transform.shear(10, 0)

        # painter.setTransform(transform)
        # super().paintEvent(event)

        # if self.title == "hubble":
        #     pixmap = QPixmap("/Users/raulmorenogines/Programming_Projects/custom_widgets/res/static/images/hubble.jpeg")
        # elif self.title == "planck":
        #     pixmap = QPixmap("/Users/raulmorenogines/Programming_Projects/custom_widgets/res/static/images/planck.jpg")
        
        pixmap = QPixmap(self.img_path)
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), pixmap)

    def mousePressEvent(self, event):
        print("clicked:", self.title)
        self.label.setStyleSheet(STYLESHEET["CustomLabel-clicked"])
        self.setStyleSheet(STYLESHEET["CustomCardWidget-clicked"])


        self.clicked_flag = True
        self.clicked_counter += 1
        self.card_selected_signal.emit(str(self.title))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        # -- Call inherited constructor
        super(MainWindow, self).__init__(parent)

        self.setGeometry(100, 100, 800, 600)

        self.central_main_widget = QWidget()
        self.setCentralWidget(self.central_main_widget)

        self.main_layout = QVBoxLayout()

        self.top_frame = QFrame()
        self.top_frame.setObjectName("customFrame")
        self.top_frame.setStyleSheet(STYLESHEET["CustomFrame"])
        self.bottom_frame = QFrame()
        self.bottom_frame.setObjectName("customFrame")
        self.bottom_frame.setStyleSheet(STYLESHEET["CustomFrame"])

        
        self.main_layout.addWidget(self.top_frame)
        self.main_layout.addWidget(self.bottom_frame)
        self.main_layout.setStretch(0, 3)
        self.main_layout.setStretch(1, 2)

        # ==== Top Frame ====
        self.top_frame_layout = QHBoxLayout()

        self.cards_container = CardsContainerWidget()
        self.card_1 = CardWidget(parent = self.cards_container,title="hubble", img_path="/Users/raulmorenogines/Programming_Projects/custom_widgets/res/static/images/hubble.jpeg")
        #self.card_1.card_selected_signal.connect(self.set_fleet)
        self.card_2 = CardWidget(parent = self.cards_container, title="planck", img_path="/Users/raulmorenogines/Programming_Projects/custom_widgets/res/static/images/planck.jpg")
        #self.card_2.card_selected_signal.connect(self.set_fleet)
        # self.card_3 = CardWidget(parent = self.cards_container, title="other", img_path="/Users/raulmorenogines/Programming_Projects/custom_widgets/res/static/images/planck.jpg")
        self.cards_container.insert_card(self.card_1)
        self.cards_container.insert_card(self.card_2)
        # self.cards_container.insert_card(self.card_3)

        self.top_frame_layout.addWidget(self.cards_container)

        self.top_frame.setLayout(self.top_frame_layout)
        # ===================

        # ==== Bottom Frame ====
        self.bottom_frame_layout = QHBoxLayout()

        self.fleet_selected_label = QLabel("-- No fleet selected --")
        style = """
            QLabel 
            {
                border-width: 0px;
                color: black;
                font-size: 64px;
            }
        """
        self.fleet_selected_label.setStyleSheet(style)
        self.fleet_selected_label.setAlignment(Qt.AlignCenter)
        self.bottom_frame_layout.addWidget(self.fleet_selected_label)

        self.bottom_frame.setLayout(self.bottom_frame_layout)
        # ===================


        self.central_main_widget.setLayout(self.main_layout)

    # def set_fleet(self, fleet:str):
    #     self.fleet_selected_label.setText(fleet)

    #     if fleet == "hubble":
    #         self.card_2.restart_position()
    #         self.card_2.clicked_flag = False
    #     elif fleet == "planck":
    #         self.card_1.restart_position()
    #         self.card_1.clicked_flag = False




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())