from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QToolBox, QLabel, QApplication, QLineEdit
import sys

STYLESHEET = """
    QToolBox::tab{
        border: 1px solid #C4C4C3;
        border-bottom-color: RGB(0, 0, 255);
    }
    QToolBox::tab:selected{
        background-color: #ffe099;
        border-top-style: none;
        border-left-style: none;
        border-right-style: none;
    }
"""

class Window(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)

        # Add toolbar and items
        toolbox = QToolBox()
        toolbox.setStyleSheet(STYLESHEET)
        layout.addWidget(toolbox, 0, 0)
        # label = QLabel()
        # toolbox.addItem(label, "Students")
        # label = QLabel()
        # toolbox.addItem(label, "Teachers")
        # label = QLabel()
        # toolbox.addItem(label, "Directors")

        # # show number of items
        # print(toolbox.count())

        # # disable tab
        # toolbox.setItemEnabled(0, False)

        # # mouseover tooltip
        # toolbox.setItemToolTip(0, "This is a tooltip")

        # # tests if items are enabled
        # print(toolbox.isItemEnabled(0))
        # print(toolbox.isItemEnabled(1))

        # # insert item
        # item = QLabel()
        # toolbox.insertItem(1, item, "Python")

        # ---------- Widget 1 Creation ------------
        # -- Create widget object
        widget_1 = QWidget()

        # -- Create layout
        layout_1 = QHBoxLayout()

        # -- Create content
        self.line_edit = QLineEdit()
        self.label = QLabel("Enter something")

        # -- Add content into layout
        layout_1.addWidget(self.label)
        layout_1.addWidget(self.line_edit)

        # -- Set layout to widget
        widget_1.setLayout(layout_1)
        # ------------------------------------------

        # --- Add widgets to tabs
        toolbox.addItem(widget_1, "Tab 1")
        label = QLabel()
        toolbox.addItem(label, "Tab 2")




app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())