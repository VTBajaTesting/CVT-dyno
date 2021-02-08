import tkinter as tk

HEIGHT = 700
WIDTH = 800

root = tk.Tk()

canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

#anchor is where widget positions from (n,e,s,w)
topframe = tk.Frame(root, bg = '#409DD7', bd = 5)
topframe.place(relx = 0.5, rely = 0.1, relwidth = 0.75, relheight = 0.1, anchor= 'n')

entry = tk.Entry(topframe, font=45)
#entry.pack(side = 'left', fill = 'both')
entry.place(relx=.01, relwidth=0.65, relheight=1)

#Put button within frame instead of root
#.pack() is how you organize the placement and size of the widgets
#Within .pack() - side moves widget to top, bottom, left, or right
#Within .pack() - fill 'both' expands widget within parameter, in this case the parameter is frame
#Within .pack() - expand = True expands widget to fill any space open within the parent widget in both x and y direction
button = tk.Button(topframe, text = "Get Weather", bg ='#DBDFE2', font=45)
#button.pack(side = 'left', fill = 'y', expand = True)
#entry.grid(row=2, column=2)
button.place(relx=.7, relwidth=0.29, relheight=1)

bottom_frame = tk.Frame(root, bg = '#409DD7', bd = 10)
bottom_frame.place(relx=0.5, rely=.3, relwidth=0.75, relheight=0.55, anchor='n')


label = tk.Label(bottom_frame, text = "This is a label")
#label.pack(side = 'left', fill = 'both')
label.place(relwidth=1, relheight=1)

root.mainloop()
