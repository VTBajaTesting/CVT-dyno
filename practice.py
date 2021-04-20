import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from tkinter import *
class run:
    def __init__(self,  window):
        self.window = window
        self.window.geometry("1920x1080")
        #self.box = Entry(window)
        x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        y= np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
        self.plot(x,y)
        #self.box.place(x = 1920//2, y = 50)
        self.saver = Button(window, text="save graph", command=plt.savefig('T2.pdf'))
        self.saver.configure(bg="red")
        self.saver.place(x = 1920//2 + 500, y = 950)
    def plot (self, x, y):
        fig = Figure(figsize=(6,6))
        a = fig.add_subplot(221)
        ax = fig.add_subplot(222)
        fig.tight_layout(pad = 3.0)
        a.scatter(x,y,color='red')
        ax.scatter(np.linspace(0,10,10), np.linspace(0,10,10),color='blue')
        a.set_ylabel("Input Speed", fontsize=14)
        a.set_xlabel("Output Shaft Speed", fontsize=14)
        ax.set_ylabel("Percent Efficiency", fontsize = 14)
        ax.set_xlabel("Output Shaft Speed", fontsize=14)

        a.set_ylim([0,10000])
        ax.set_ylim([0,100])
        a.set_xlim([0,2200])
        ax.set_xlim([0,2200])
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.get_tk_widget().place(x = 1920//2 + 250, y = 50)
        canvas.draw()
    #def save():
class params:
    def __init__(self, window):
        self.window = window
        self.go = Button(window, text="GO!", command=self.next_window)
        self.go.configure(bg="green")
        self.abort = Button(window, text="Abort Test", command=self.estop)
        self.abort.configure(bg="red")
        #self.go.pack()
        #self.abort.pack()

        self.speed_out = None
        self.torque_in = None
        self.slabel = StringVar()
        self.slabel.set("Enter output speeds:")
        self.tlabel = StringVar()
        self.tlabel.set("Enter input torques:")
        self.speed_entry = Entry(window, textvariable=self.slabel)
        self.torque_entry = Entry(window, textvariable=self.tlabel)
        self.speed_entry.place(x = 1920//2 - 200, y = 50)
        self.torque_entry.place(x = 1920//2 + 100, y = 50)
        self.go.place(x = 1920//2 - 50, y = 500)
        self.abort.place(x = 1920//2 + 75, y = 500)
        #self.speed_entry.pack()
        #self.torque_entry.pack()
    def next_window(self):
        self.speed_out = [int(i) for i in self.speed_entry.get()[1:-1].split(',')]
        self.torque_in = [int(i) for i in self.torque_entry.get()[1:-1].split(',')]
        print(self.speed_out)
        print(self.torque_in)
        self.new = Toplevel(self.window)
        self.app = run(self.new)
    def estop(self):
        print("estop")
window= Tk()
window.geometry("1920x1080")
print('yyeee')
start= params (window)
window.mainloop()