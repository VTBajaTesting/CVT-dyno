import tkinter as tk
import matplotlib
from matplotlib import pyplot as plt
from tkinter.ttk import *
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def myCLick():
    root.configure(background = 'grey')
def clearFrame():
    for widget in root.winfo_children():
        widget.destroy()
        print('removed')
        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
def dummy(root):
    root.after(1000, dummy, root)
    print()
def savefig():
    plt.savefig('T2.pdf')
def run_t2():
    clearFrame()
    
    figure = Figure(figsize=(5, 4), dpi=100)
    plot = figure.add_subplot(1, 1, 1)
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.get_tk_widget().grid(row=0, column=0)
    x = [0.1, 0.2, 0.3]
    y = [-0.1, -0.2, -0.3]
    plot.set_ylabel('Input Speed - RPM')
    plot.set_xlabel('Output Shaft Speed (RPM)')
    plot.plot(x, y, color="blue", marker="x", linestyle="")
    save = tk.Button(text="Save graph", padx =10, command=savefig, font=("Arial", 35), bg="red")
    back = tk.Button(text="Back", padx =10, command=load_p1, font=("Arial", 35), bg="red")
    back.grid(row = 2, column = 1, sticky='E')
    save.grid(row=2, column=2)
def load_p1():
    clearFrame()
    blank_space1 = tk.Label(text = '     ', bg = 'grey', font = (None, 30))

    torqueLbl = tk.Label(text="Set Input Torque", font=("Arial", 35), bg="grey")

    torqueEntry = tk.Entry(font=("Arial", 35), width = 10)
    torqueUnit = tk.Label(text="N*M", font=("Arial", 35), bg="grey")

    speedLbl = tk.Label(text="Set Output Speed", font=("Arial", 35), bg="grey")

    speedEntry = tk.Entry(font=("Arial", 35), width = 10)
    speedUnit = tk.Label(text="N*M", font=("Arial", 35), bg="grey")

    runButton = tk.Button(text="Run Test", padx =10, command= run_t2, font=("Arial", 35), bg="green")
    stopButton = tk.Button(text="Stop Test", padx =10, command=myCLick, font=("Arial", 35), bg="red")

    backButton = tk.Button(text="Back", padx =10, command=myCLick, font=("Arial", 20), bg="red")



    root.columnconfigure(0, weight=1,)


    ## Place widgets


    blank_space1.grid(row=0, pady=(50,50))


    torqueLbl.grid(row=1, column=2, sticky="E", padx=(10, 400))


    torqueEntry.grid(row=3, column=2, padx=(50, 400))
    torqueUnit.grid(row=3, column=2, padx=(50, 0))

    speedLbl.grid(row = 4, column = 2, sticky='E', padx=(10,400))
    speedEntry.grid(row=5, column=2, padx=(50, 400))
    speedUnit.grid(row=5, column=2, padx=(50, 0))

    runButton.grid(row=6, column=0, pady=(100,25), sticky='E')
    stopButton.grid(row=6, column=1, pady=(100,25), sticky='W')

    backButton.grid(row=7, column=0, sticky='W', padx=(50, 0))

    root.configure(background = 'grey')
    root.attributes('-fullscreen', True)

    #dummy(root)
    root.mainloop()

def first_page(root):
    blank_space1 = tk.Label(text = '     ', bg = 'grey', font = (None, 30))

    torqueLbl = tk.Label(text="Set Input Torque", font=("Arial", 35), bg="grey")

    torqueEntry = tk.Entry(font=("Arial", 35), width = 10)
    torqueUnit = tk.Label(text="N*M", font=("Arial", 35), bg="grey")

    speedLbl = tk.Label(text="Set Output Speed", font=("Arial", 35), bg="grey")

    speedEntry = tk.Entry(font=("Arial", 35), width = 10)
    speedUnit = tk.Label(text="N*M", font=("Arial", 35), bg="grey")

    runButton = tk.Button(text="Run Test", padx =10, command= run_t2, font=("Arial", 35), bg="green")
    stopButton = tk.Button(text="Stop Test", padx =10, command=myCLick, font=("Arial", 35), bg="red")

    backButton = tk.Button(text="Back", padx =10, command=myCLick, font=("Arial", 20), bg="red")



    root.columnconfigure(0, weight=1,)


    ## Place widgets


    blank_space1.grid(row=0, pady=(50,50))


    torqueLbl.grid(row=1, column=2, sticky="E", padx=(10, 400))


    torqueEntry.grid(row=3, column=2, padx=(50, 400))
    torqueUnit.grid(row=3, column=2, padx=(50, 0))

    speedLbl.grid(row = 4, column = 2, sticky='E', padx=(10,400))
    speedEntry.grid(row=5, column=2, padx=(50, 400))
    speedUnit.grid(row=5, column=2, padx=(50, 0))

    runButton.grid(row=6, column=0, pady=(100,25), sticky='E')
    stopButton.grid(row=6, column=1, pady=(100,25), sticky='W')

    backButton.grid(row=7, column=0, sticky='W', padx=(50, 0))

    root.configure(background = 'grey')
    root.attributes('-fullscreen', True)
    
    root.mainloop()
#dummy(root)
if __name__ == '__main__':
    root = tk.Tk()
    first_page(root)
## Create widgets





#secondarySpeed

#output torque