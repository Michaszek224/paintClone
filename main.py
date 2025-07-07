from tkinter import *
from tkinter import ttk
from tkinter import simpledialog

prev_x = None
prev_y = None
canvas = None

#Standard variables
line_width = 2
backgroundColor = "white"
color = "black"

def on_click(event):
    '''Handle mouse click events and print coordinates.'''
    drawing(event)
    # Function to make it more fancy :D
    
def drawing(event):
    '''Drawing function'''
    global prev_x, prev_y, canvas, line_width, color
    current_x, current_y = event.x, event.y
    # print("Coordinates: ({}, {})".format(current_x, current_y))
    if prev_x is not None and prev_y is not None:
        # print("Drawing line from ({}, {}) to ({}, {})".format(prev_x, prev_y, current_x, current_y))
        canvas.create_line(prev_x, prev_y, current_x, current_y, fill=color, width=line_width, joinstyle="round", capstyle="round")
    prev_x, prev_y = current_x, current_y
    #Drawing a line betweeen previous and current coordinates
    
def on_release(event):
    '''Handle mouse release events.'''
    global prev_x, prev_y
    # print("Mouse released at ({}, {})".format(event.x, event.y))
    prev_x, prev_y = None, None
    # REset the previous coordinates to prevent drawing lines when clicking after releasing the mouse button

def clear():
    '''Clear the canvas.'''
    global canvas
    canvas.delete("all")
    # print("Canvas cleared")
    # Clear the canvas and print a message

def widthMenu():
    '''Change the width of the lines drawn.'''
    global line_width
    width = simpledialog.askinteger("Line Width", "Enter line width:", minvalue=1, maxvalue=100)
    if width is not None:
        line_width = width
        # Change the width of the lines drawn on the canvas
        
def colorMenu():
    '''Change the color of the lines drawn.'''
    global canvas, color
    color = simpledialog.askstring("Line Color", "Enter line color (e.g., 'red', '#FF0000'):", initialvalue="black")
    
def backgroundMenu():
    '''Change the background color of the canvas.'''
    global canvas, backgroundColor
    backgroundColor = simpledialog.askstring("Background Color", "Enter background color (e.g., 'white', '#FFFFFF'):", initialvalue="white")
    canvas.config(bg=backgroundColor)
    # Change the background color of the canvas

root = Tk()
frm = ttk.Frame(root)
frm.grid(row = 0, column = 0, sticky = "NSEW")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#Buttons section
ttk.Button(frm, text="Clear", command=clear).grid(row=0, column=0, sticky="EW")
ttk.Button(frm, text="Width", command=widthMenu).grid(row=0, column=1, sticky="EW")
ttk.Button(frm, text="Color", command=colorMenu).grid(row=1, column=0, sticky="EW")
ttk.Button(frm, text="Background", command=backgroundMenu).grid(row=1, column=1, sticky="EW")

# Create a canvas for drawing with a white background
canvas = Canvas(frm, bg=backgroundColor)
canvas.grid(row=2, column=0, columnspan=99, sticky="NSEW")

# Configure the grid layout for the frame
frm.grid_rowconfigure(0, weight=0)
frm.grid_rowconfigure(1, weight=0)
frm.grid_rowconfigure(2, weight=1)
frm.grid_columnconfigure(0, weight=1)
frm.grid_columnconfigure(1, weight=1)

# Set the window to full screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("{}x{}".format(screen_width, screen_height))

# Binding mouse events to the canvbas
root.bind("<Button-1>", on_click) # Left mouse click
root.bind("<B1-Motion>", on_click) # Left mouse drag
root.bind("<ButtonRelease-1>", on_release) # Left mouse release

root.mainloop()