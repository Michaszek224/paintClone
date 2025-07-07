from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import simpledialog
from tkinter import Toplevel, Scale, HORIZONTAL, Label, Button

prev_x = None
prev_y = None
canvas = None

#Standard variables
lineWidth = 2
backgroundColor = "white"
color = "black"

def on_click(event):
    '''Handle mouse click events and print coordinates.'''
    drawing(event)
    # Function to make it more fancy :D
    
def drawing(event):
    '''Drawing function'''
    global prev_x, prev_y, canvas, lineWidth, color
    current_x, current_y = event.x, event.y
    # print("Coordinates: ({}, {})".format(current_x, current_y))
    if prev_x is not None and prev_y is not None:
        # print("Drawing line from ({}, {}) to ({}, {})".format(prev_x, prev_y, current_x, current_y))
        canvas.create_line(prev_x, prev_y, current_x, current_y, fill=color, width=lineWidth, joinstyle="round", capstyle="round")
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
    # Delete all items from the canvas

        
def widthMenu():
    '''Open a dialog to select the line width.'''
    global lineWidth
    
    def applyWidth():
        nonlocal slider
        global lineWidth
        lineWidth = slider.get()
        win.destroy()
        
    win = Toplevel(root)
    win.title("Select Line Width")
    win.geometry("300x150")
    win.resizable(False, False)
    
    win.transient(root)
    win.grab_set()
    win.focus_set()
    
    Label(win, text="Adjust Line Width:").pack(pady=10)
    
    slider = Scale(win, from_=1, to=20, orient=HORIZONTAL, length=250)
    slider.set(lineWidth)  # Set the current line width
    slider.pack()
    
    Button(win, text="Apply", command=applyWidth).pack(pady=5)
        
def colorMenu():
    '''Change the color of the lines drawn.'''
    global color
    selected_color = colorchooser.askcolor(title="Select Line Color")
    if selected_color[1] is not None:
        color = selected_color[1]
    
def backgroundMenu():
    '''Change the background color of the canvas.'''
    global canvas, backgroundColor
    selected_color = colorchooser.askcolor(title="Select Background Color")
    if selected_color[1] is not None:
        backgroundColor = selected_color[1]
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