from pathlib import Path
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys

class PicoScopeApp(QMainWindow):
    def __init__(self, device):
        # Initialize the main window
        # super() is used to call the __init__() method of the parent class
        super().__init__()
        self.device = device
        self.setWindowTitle("PicoScope Real-Time Graph")

        # Set the geometry of the main window
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # FigureCanvas is the area on the window where the plot is drawn
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)
        layout.addLayout(self.button_layout)

        self.start_button.clicked.connect(self.start_plotting)
        self.stop_button.clicked.connect(self.stop_plotting)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)

    def start_plotting(self):
        self.device.initialize()
        self.timer.start(100)  # Update every 100 ms (10 times per second)

    def stop_plotting(self):
        self.timer.stop()
        self.device.finalize()

    def update_plot(self):
        self.device.run_block_capture()
        data_a, data_b = self.device.collect_data()

        time = np.linspace(0, (len(data_a) - 1) * self.device.time_interval, len(data_a))

        self.ax.clear()
        self.ax.plot(time, data_a, label='Channel A')
        self.ax.plot(time, data_b, label='Channel B')
        self.ax.set_xlabel("Time (ns)")
        self.ax.set_ylabel("Voltage (mV)")
        self.ax.legend()
        self.ax.legend(loc='right', bbox_to_anchor=(1, 0.5))
        self.canvas.draw()

if __name__ == "__main__":
    from Controller.initilialise import PicoScopeDevice  # Importing the device class
    app = QApplication(sys.argv)
    device = PicoScopeDevice()
    main = PicoScopeApp(device)
    main.show()
    sys.exit(app.exec_())