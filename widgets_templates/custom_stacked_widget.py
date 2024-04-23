########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## IMPORTS
########################################################################
import os

########################################################################
## MODULE UPDATED TO USE QT.PY
########################################################################
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys

"""
This is an extension of QStackedWidget which adds transition animation
And Navigation Functions to
your QStackedWidget widgets
You can customize the animations using a JSon file or Python statements
"""


########################################################################
## QStackedWidget Class
########################################################################
class QCustomQStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super(QCustomQStackedWidget, self).__init__(parent)

        ########################################################################
        ## Initialize Default Values
        ########################################################################
        # Fade transition
        self.fadeTransition = False
        # Slide transition
        self.slideTransition = False
        # Default transition direction
        self.transitionDirection = QtCore.Qt.Vertical
        # Default transition animation time
        self.transitionTime = 1000
        # Default fade animation time
        self.fadeTime = 1000
        # Default transition animation easing curve
        self.transitionEasingCurve = QtCore.QEasingCurve.BezierSpline
        # Default transition animation easing curve
        self.fadeEasingCurve = QtCore.QEasingCurve.Linear
        # Default current widget index
        self.currentWidget = 0
        # Default next widget index
        self.nextWidget = 0
        # Default widget position
        self._currentWidgetPosition = QtCore.QPoint(0, 0)
        # Default boolean for active widget
        self.widgetActive = False


    ########################################################################
    ## Function to update transition direction
    ########################################################################
    def setTransitionDirection(self, direction):
        self.transitionDirection = direction

    ########################################################################
    ## Function to update transition speed
    ########################################################################
    def setTransitionSpeed(self, speed):
        self.transitionTime = speed

    ########################################################################
    ## Function to update fade speed
    ########################################################################
    def setFadeSpeed(self, speed):
        self.fadeTime = speed

    ########################################################################
    ## Function to update transition easing curve
    ########################################################################
    def setTransitionEasingCurve(self, aesingCurve):
        self.transitionEasingCurve = aesingCurve

    ########################################################################
    ## Function to update fade easing curve
    ########################################################################
    def setFadeCurve(self, aesingCurve):
        self.fadeEasingCurve = aesingCurve

    ########################################################################
    ## Function to update fade animation playing state
    ########################################################################
    def setFadeTransition(self, fadeState):
        if isinstance(fadeState, bool):
            self.fadeTransition = fadeState
        else:
            raise Exception("setFadeTransition() only accepts boolean variables")

    ########################################################################
    ## Function to update slide  playing state
    ########################################################################
    def setSlideTransition(self, slideState):
        if isinstance(slideState, bool):
            self.slideTransition = slideState
        else:
            raise Exception("setSlideTransition() only accepts boolean variables")

    ########################################################################
    ## Function to transition to previous widget
    ########################################################################
    def slideToPreviousWidget(self):
        currentWidgetIndex = self.currentIndex()
        if currentWidgetIndex > 0:
            self.slideToWidgetIndex(currentWidgetIndex - 1)

    ########################################################################
    ## Function to transition to next widget
    ########################################################################
    def slideToNextWidget(self):
        currentWidgetIndex = self.currentIndex()
        if currentWidgetIndex < (self.count() - 1):
            self.slideToWidgetIndex(currentWidgetIndex + 1)


    ########################################################################
    ## Function to transition to a given widget index
    ########################################################################
    def slideToWidgetIndex(self, index):
        if index > (self.count() - 1):
            index = index % self.count()
        elif index < 0:
            index = (index + self.count()) % self.count()
        if self.slideTransition:
            self.slideToWidget(self.widget(index))
        else:
            self.setCurrentIndex(index)

    ########################################################################
    ## Function to transition to a given widget
    ########################################################################
    def slideToWidget(self, newWidget):
        # If the widget is active, exit the function
        if self.widgetActive:
            return

        # Update widget active bool
        self.widgetActive = True

        # Get current and next widget index
        _currentWidgetIndex = self.currentIndex()
        _nextWidgetIndex = self.indexOf(newWidget)

        # If current widget index is equal to next widget index, exit function
        if _currentWidgetIndex == _nextWidgetIndex:
            self.widgetActive = False
            return

        # Get X and Y position of QStackedWidget
        offsetX, offsetY = self.frameRect().width(), self.frameRect().height()
        # Set the next widget geometry
        self.widget(_nextWidgetIndex).setGeometry(self.frameRect())

        # Set left right(horizontal) or up down(vertical) transition
        if not self.transitionDirection == QtCore.Qt.Horizontal:
            if _currentWidgetIndex < _nextWidgetIndex:
                # Down up transition
                offsetX, offsetY = 0, -offsetY
            else:
                # Up down transition
                offsetX = 0
        else:
            # Right left transition
            if _currentWidgetIndex < _nextWidgetIndex:
                offsetX, offsetY = -offsetX, 0
            else:
                # Left right transition
                offsetY = 0

        nextWidgetPosition = self.widget(_nextWidgetIndex).pos()
        currentWidgetPosition = self.widget(_currentWidgetIndex).pos()
        self._currentWidgetPosition = currentWidgetPosition

        # Animate transition
        offset = QtCore.QPoint(offsetX, offsetY)
        self.widget(_nextWidgetIndex).move(nextWidgetPosition - offset)
        self.widget(_nextWidgetIndex).show()
        self.widget(_nextWidgetIndex).raise_()

        anim_group = QtCore.QParallelAnimationGroup(
            self, finished=self.animationDoneSlot
        )

        for index, start, end in zip(
            (_currentWidgetIndex, _nextWidgetIndex),
            (currentWidgetPosition, nextWidgetPosition - offset),
            (currentWidgetPosition + offset, nextWidgetPosition)
        ):
            animation = QtCore.QPropertyAnimation(
                self.widget(index),
                b"pos",
                duration=self.transitionTime,
                easingCurve=self.transitionEasingCurve,
                startValue=start,
                endValue=end,
            )
            anim_group.addAnimation(animation)

        self.nextWidget = _nextWidgetIndex
        self.currentWidget = _currentWidgetIndex

        self.widgetActive = True
        anim_group.start(QtCore.QAbstractAnimation.DeleteWhenStopped)

        # Play fade animation
        if self.fadeTransition:
            FadeWidgetTransition(self, self.widget(_currentWidgetIndex), self.widget(_nextWidgetIndex))

    ########################################################################
    ## Function to hide old widget and show new widget after animation is done
    ########################################################################
    def animationDoneSlot(self):
        self.setCurrentIndex(self.nextWidget)
        self.widget(self.currentWidget).hide()
        self.widget(self.currentWidget).move(self._currentWidgetPosition)
        self.widgetActive = False

    ########################################################################
    ## Function extending the QStackedWidget setCurrentWidget to animate transition
    ########################################################################
    def setCurrentWidget(self, widget):
        currentIndex = self.currentIndex()
        nextIndex = self.indexOf(widget)
        if self.currentIndex() == self.indexOf(widget):
            return
        if self.slideTransition:
            self.slideToWidgetIndex(nextIndex)

        if self.fadeTransition:
            FadeWidgetTransition(self, self.widget(self.currentIndex()), self.widget(self.indexOf(widget)))
        
            # if not self.slideTransition:
            #     self.setCurrentIndex(0)
            
        if not self.slideTransition and not self.fadeTransition:
            self.setCurrentIndex(nextIndex)

########################################################################
## Fade widget class
########################################################################
class FadeWidgetTransition(QWidget):
    def __init__(self, animationSettings, oldWidget, newWidget):
        QWidget.__init__(self, animationSettings.widget(0))

        self.oldPixmap = QPixmap(oldWidget.size())
        oldWidget.render(self.oldPixmap)
        self.pixmapOpacity = 1

        self.animationSettings = animationSettings
        self.newWidget = newWidget

        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animateOldWidget)
        self.timeline.finished.connect(self.animationFinished)
        self.timeline.setDuration(animationSettings.fadeTime)
        self.timeline.setEasingCurve(animationSettings.fadeEasingCurve)
        self.timeline.start()
        
        self.resize(oldWidget.size())
        self.show()

        if not animationSettings.slideTransition:
            animationSettings.setCurrentIndex(0)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        # painter.setOpacity(self.pixmapOpacity)
        try:
            painter.setOpacity(self.pixmapOpacity)
        except Exception:
            self.pixmapOpacity = 1
            # painter.setOpacity(self.pixmapOpacity)

        
        painter.drawPixmap(0, 0, self.oldPixmap)
        painter.end()

    def animateOldWidget(self, value):
        self.pixmapOpacity = 1.0 - value
        self.repaint()

    def animationFinished(self):
        self.close()
        FadeOutWidgetTransition(self.animationSettings, self.animationSettings.widget(0), self.newWidget)

class FadeOutWidgetTransition(QWidget):
    def __init__(self, animationSettings, oldWidget, newWidget):
        QWidget.__init__(self, newWidget)

        self.oldPixmap = QPixmap(oldWidget.size())
        oldWidget.render(self.oldPixmap)
        self.pixmapOpacity = 1

        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animateOldWidget)
        self.timeline.finished.connect(self.animationFinished)
        self.timeline.setDuration(animationSettings.fadeTime)
        self.timeline.setEasingCurve(animationSettings.fadeEasingCurve)
        self.timeline.start()
        
        self.resize(oldWidget.size())
        self.show()

        if not animationSettings.slideTransition:
            nextIndex = animationSettings.indexOf(newWidget)
            animationSettings.setCurrentIndex(nextIndex)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmapOpacity)
        painter.drawPixmap(0, 0, self.oldPixmap)
        painter.end()

    def animateOldWidget(self, value):
        self.pixmapOpacity = 1.0 - value
        self.repaint()

    def animationFinished(self):
        self.close()

########################################################################
## CUSTOM QCheckBox
########################################################################
class QCustomCheckBox(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Get geometry
        # print(self.geometry())

        # self.setFixedSize(50, 28)
        # self.setMinimumSize(QSize(50, 28))
        self.setCursor(Qt.PointingHandCursor)

        # Check if a QApplication instance already exists
        if QApplication.instance():
            app = QApplication.instance()
        else:
            app = QApplication([])  # Create a new QApplication instance if it doesn't exist


        # Get the default palette
        palette = app.palette()
            
        # Get the default background color
        bgColor = palette.color(QPalette.Window)
        # Get the default text color (assuming this is your "circle_color")
        circleColor = palette.color(QPalette.Text)
        # Get the default highlight color (assuming this is your "active_color")
        activeColor = palette.color(QPalette.Highlight)

        # COLORS
        self.bgColor = bgColor
        self.circleColor = circleColor
        self.activeColor = activeColor

        # Animation
        self.animationEasingCurve = QEasingCurve.OutBounce
        self.animationDuration = 300

        self.pos = 3
        self.animation = QPropertyAnimation(self, b"position")
        self.animation.setEasingCurve(self.animationEasingCurve)
        self.animation.setDuration(self.animationDuration)
        self.stateChanged.connect(self.setup_animation)

        # Create a QLabel to display the text
        self.label = QLabel(self)
        # self.label.setContentsMargins(0, 0, 0, 0)  # Set contents margins to 0 to remove spacing
        self.label.setWordWrap(True)

    ########################################################################
    # Customize QCustomCheckBox
    ########################################################################
    def customizeQCustomCheckBox(self, **customValues):
        if "bgColor" in customValues:
            self.bgColor = customValues["bgColor"]
        
        if "circleColor" in customValues:
            self.circleColor = customValues["circleColor"]

        if "activeColor" in customValues:
            self.activeColor = customValues["activeColor"]

        if "animationEasingCurve" in customValues:
            self.animationEasingCurve = customValues["animationEasingCurve"]
            self.animation.setEasingCurve(self.animationEasingCurve)

        if "animationDuration" in customValues:
            self.animationDuration = customValues["animationDuration"]
            self.animation.setDuration(self.animationDuration)

        self.update()


    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Update checkbox size
        # Update label position and width
        labelx = self.height() * 2.1 + 2
        labely = 0
        # self.label.setGeometry(labelx, labely, labelwidth, labelheight)
        self.label.setGeometry(labelx, labely, 0, 0)  # Set initial dimensions to 0, 0
        self.label.adjustSize()  # Adjust the size based on the content


    def setText(self, text):
        super().setText(text)
        self.label.setText(text)

    def position(self):
        return self.pos

    def position(self, pos):
        self.pos = pos
        self.update()

    # START STOP ANIMATION
    def setup_animation(self, value):
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.height() + 2)
        else:
            self.animation.setEndValue(0)
        self.animation.start()
    
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # SET PEN
        p.setPen(Qt.NoPen)

        # DRAW RECT
        rect = QRect(0, 0, self.height() * 2.2, self.height())        

        if not self.isChecked():
            p.setBrush(QColor(self.bgColor))
            p.drawRoundedRect(0, 0, self.height() * 2.1, self.height(), self.height() * .5, self.height() * .5)
            
            p.setBrush(QColor(self.circleColor))
            p.drawEllipse(self.pos, 0, self.height(), self.height())
        else:
            p.setBrush(QColor(self.activeColor))
            p.drawRoundedRect(0, 0, self.height() * 2.1, self.height(), self.height() * .5, self.height() * .5)

            p.setBrush(QColor(self.circleColor))
            p.drawEllipse(self.pos, 0, self.height(), self.height())

        p.end()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        # -- Call inherited constructor
        super(MainWindow, self).__init__(parent)

        # -- Configure main window
        self.setWindowTitle("Customized widgets")
        self.setGeometry(100, 100, 800, 600)  # (x, y, width, height)

        # -- Create Central widget for main window
        self.main_central_widget = QWidget()
        self.setCentralWidget(self.main_central_widget)

        # -- Create main layout
        self.main_window_vlayout = QVBoxLayout()

        # -- Create stacked widgets
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        layout = QFormLayout()
        layout.addRow("Name",QLineEdit())
        layout.addRow("Address",QLineEdit())
        self.stack1.setLayout(layout)

        layout_2 = QHBoxLayout()
        main_frame = QFrame()
        _style = f"""
        QFrame {{
            border: 1px solid;
            border-radius: 5px;
        }}
        QLabel{{
            font-size: 14px;
    		color: #2F4F4F;
            border: none;
        }} 
        """

        main_frame.setStyleSheet(_style)

        layout_2_1 = QVBoxLayout()
        label_1 = QLabel("Data")
        label_2 = QLabel("Data 1")
        btn_1 = QPushButton("run")
        layout_2_1.addWidget(label_1)
        layout_2_1.addWidget(label_2)
        layout_2_1.addWidget(btn_1)

        main_frame.setLayout(layout_2_1)
        layout_2.addWidget(main_frame)
        self.stack2.setLayout(layout_2)


        layout_s3 = QHBoxLayout()
        layout_s3.addWidget(QLabel("subjects"))
        layout_s3.addWidget(QCheckBox("Physics"))
        layout_s3.addWidget(QCheckBox("Maths"))
        self.stack3.setLayout(layout_s3)

        # self.Stack = QStackedWidget(self)
        self.Stack = QCustomQStackedWidget(self)
        self.Stack.addWidget (self.stack1)
        self.Stack.addWidget (self.stack2)
        self.Stack.addWidget (self.stack3)

        self.next_btn = QPushButton("Next")
        # self.custom_check_box = QCustomCheckBox(self)

        # -- Add widgets to layout
        self.main_window_vlayout.addWidget(self.Stack)
        # self.main_window_vlayout.addWidget(self.custom_check_box)
        self.main_window_vlayout.addWidget(self.next_btn)

        # -- Set layout to main window
        self.main_central_widget.setLayout(self.main_window_vlayout)

        self.next_btn.clicked.connect(self._next_page)

    def _next_page(self):
        index = self.Stack.currentIndex()

        if index == 2:
            next_index = 0
        else:
            next_index = index + 1
        # self.Stack.setCurrentIndex(next_index)
        
        if next_index == 0:
            self.Stack.slideToWidget(self.stack1)
        elif next_index == 1:
            self.Stack.slideToWidget(self.stack2)
        elif next_index == 2:
            self.Stack.slideToWidget(self.stack3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())