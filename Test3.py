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
    plot.set_ylabel('Percent Efficiency')
    plot.set_xlabel('Output Shaft Speed (RPM)')
    plot.plot(x, y, color="blue", marker="x", linestyle="")







## Create widgets
blank_space1 = tk.Label(text = '     ', bg = 'grey', font = (None, 30))


torqueLbl = tk.Label(text="Set Input Torque", font=("Arial", 35), bg="grey")




torqueEntry = tk.Entry(font=("Arial", 35), width = 10)
torqueUnit = tk.Label(text="N*M", font=("Arial", 35), bg="grey")

runButton = tk.Button(text="Run Test", padx =10, command= run_t6, font=("Arial", 35), bg="green")
stopButton = tk.Button(text="Stop Test", padx =10, command=myCLick, font=("Arial", 35), bg="red")

backButton = tk.Button(text="Back", padx =10, command=myCLick, font=("Arial", 20), bg="red")



root.columnconfigure(0, weight=1,)


## Place widgets


blank_space1.grid(row=0, pady=(50,50))








runButton.grid(row=4, column=0, pady=(100,25), sticky='W', padx=(700, 0))
stopButton.grid(row=4, column=1, pady=(100,25), sticky='W',padx=(0,710))
torqueEntry.grid(row=3, column=0, sticky='EW', columnspan=2, padx=(760,760))
torqueUnit.grid(row=3, column=1, sticky='W', padx=(150,0))
backButton.grid(row=5, column=0, pady=(450,25), sticky='W', padx=(50, 0))
torqueLbl.grid(row=1, column=0, sticky='EW', columnspan=2, padx=(760,760))
root.configure(background = 'grey')
root.attributes('-fullscreen', True)


root.mainloop()




#secondarySpeed

#output torque