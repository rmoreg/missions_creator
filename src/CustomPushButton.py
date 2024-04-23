from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QColor
from PyQt5 import QtCore
class CustomPushButton(QPushButton):
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