import sys
from PySide2.QtWidgets import QApplication,QWidget,QDoubleSpinBox,QHBoxLayout,QVBoxLayout,QLabel,QLineEdit,QPushButton,QMessageBox
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide2.QtCore import Slot
from matplotlib.backends.backend_qt5agg import FigureCanvas
import numpy as np
import re
class Plotter(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Plotter")
        self.form = FigureCanvas(Figure(figsize = (10,10)))
        self.twdD_plotter = self.form.figure.subplots()
        self.min = QDoubleSpinBox()
        self.min.setRange(-10,10)
        self.mn_label = QLabel(text="min")
        self.max = QDoubleSpinBox()
        self.max.setRange(-10,10)
        self.max_label = QLabel(text="max")
        self.min.setValue(-10)
        self.max.setValue(10)
        self.error_msg = QMessageBox()
        self.fn = QLineEdit()
        self.fn_label = QLabel(text="Function")
        self.ok = QPushButton(text="OK")

        layout_1 = QVBoxLayout()
        layout_1.addWidget(self.mn_label)
        layout_1.addWidget(self.min)
        layout_1.addWidget(self.max_label)
        layout_1.addWidget(self.max)

        layout_2 = QVBoxLayout()
        layout_2.addWidget(self.fn_label)
        layout_2.addWidget(self.fn)
        layout_2.addWidget(self.ok)

        user_layout = QVBoxLayout()
        user_layout.addWidget(self.form)
        user_layout.addLayout(layout_1)
        user_layout.addLayout(layout_2)
        self.setLayout(user_layout)

        self.ok.clicked.connect(lambda x: self.listener(1))
        self.listener(0)

    def listener(self,idx):
        min = self.min.value()
        max = self.max.value()

        if min >=max:
            self.error_msg.setText("min x is greater than or equal max x")
            self.error_msg.show()
            return
        if idx !=0:
            x = np.linspace(min, max)
            try:
                y = preprocessing_fn(self.fn.text(),x)
            except:
                self.error_msg.setWindowTitle("Function is WRONG!")
                self.error_msg.show()
                return
            self.twdD_plotter.clear()
            self.twdD_plotter.plot(x,y)
            self.form.draw()

operators = [
    'x',
    'sin',
    'cos',
    'tan',
    'sqrt',
    '/',
    '+',
    '*',
    '^',
    '-'
]

operators_to_np = {
    'sin': 'np.sin',
    'cos': 'np.cos',
    'sqrt': 'np.sqrt',
    'tan': 'np.tan',
    '^': '**'
}

def preprocessing_fn(str,x):
    for word in re.findall('[a-zA-Z_]+', str):
        if word not in operators:
            raise ValueError(
                f"'{word}' is forbidden to use in math expression.\n"
            )

    for old, new in operators_to_np.items():
        str = str.replace(old, new)

    def process(x):    
        return eval(str)
    return process(x)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Plotter()
    w.show()
    sys.exit(app.exec_())
