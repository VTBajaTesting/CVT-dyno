import numpy as np
import sys
import os
def plot_data(x:np.ndarray, y:np.ndarray, xlabel, ylabel):
    """
    Creates a matplotlib plot with all the bells and whistles
    x       - the x axis data
    y       - the y axis data
    xlabel  - a label for the x axis
    ylabel  - a label for the y axis
    """
    from matplotlib.backends.qt_compat import QtWidgets
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
    from matplotlib.figure import Figure
    class ApplicationWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super().__init__()
            self._main = QtWidgets.QWidget()
            self.setCentralWidget(self._main)

            layout = QtWidgets.QVBoxLayout(self._main)
            static_canvas = FigureCanvas(Figure(figsize=(6,6)))
            layout.addWidget(static_canvas)
            self.addToolBar(NavigationToolbar(static_canvas, self))

            self.static_ax = static_canvas.figure.subplots()
            self.static_ax.plot(x,y,'.')
            self.static_ax.set_xlabel(xlabel)
            self.static_ax.set_ylabel(ylabel)
            self.static_ax.set_title(ylabel + ' as a function of ' + xlabel)
            self.static_canvas.figure.savefig('/media/usb1/DYNODATA/drive/plot'+str(len(os.listdir('/media/usb1/DYNODATA/drive/test')))+'.csv')
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
