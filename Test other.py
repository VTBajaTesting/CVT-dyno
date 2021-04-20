import tkinter as tk
import matplotlib
from tkinter.ttk import *
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
root = tk.Tk()

def myCLick():
    root.configure(background = 'grey')
def clearFrame():
    for widget in root.winfo_children():
        widget.destroy()

        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
def run_t6():
    clearFrame()
    figure = Figure(figsize=(10, 8), dpi=100)
    plot = figure.add_subplot(1, 1, 1)
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.get_tk_widget().grid(row=0, column=0)
    x = [0.1, 0.2, 0.3]
    y = [-0.1, -0.2, -0.3]
    plot.set_ylabel('Output Shaft Torque (N*m)')
    plot.set_xlabel('Output Shaft Speed (RPM)')
    plot.plot(x, y, color="blue", marker="x", linestyle="")







## Create widgets
blank_space1 = tk.Label(text = '     ', bg = 'grey', font = (None, 30))

speedLbl = tk.Label(text="Set Secondary Speed", font=("Arial", 35), bg="grey")
torqueLbl = tk.Label(text="Set Input Torque", font=("Arial", 35), bg="grey")


secondarySpeed = tk.Entry(font=("Arial", 35), width = 10)
speedUnit = tk.Label(text="RPM", font=("Arial", 35), bg="grey")
torqueEntry = tk.Entry(font=("Arial", 35), width = 10)
torqueUnit = tk.Label(text="N*M", font=("Arial", 35), bg="grey")

runButton = tk.Button(text="Run Test", padx =10, command= run_t6, font=("Arial", 35), bg="green")
stopButton = tk.Button(text="Stop Test", padx =10, command=myCLick, font=("Arial", 35), bg="red")

backButton = tk.Button(text="Back", padx =10, command=myCLick, font=("Arial", 20), bg="red")



root.columnconfigure(0, weight=1,)


## Place widgets


blank_space1.grid(row=0, pady=(50,50))
speedLbl.grid(row=1, column=0, sticky="W", padx=(400, 10))

torqueLbl.grid(row=1, column=2, sticky="E", padx=(10, 400))

secondarySpeed.grid(row=3, column=0, pady=(25, 25), padx=(200,0))
speedUnit.grid(row=3, column=0, pady=(25, 25), sticky='E', padx=(0,75))
torqueEntry.grid(row=3, column=2, padx=(50, 400))
torqueUnit.grid(row=3, column=2, padx=(50, 0))


runButton.grid(row=4, column=0, pady=(100,25), sticky='E')
stopButton.grid(row=4, column=1, pady=(100,25), sticky='W')

backButton.grid(row=5, column=0, pady=(450,25), sticky='W', padx=(50, 0))

root.configure(background = 'grey')
root.attributes('-fullscreen', True)


root.mainloop()




#secondarySpeed

#output torque