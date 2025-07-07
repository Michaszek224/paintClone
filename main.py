from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import Toplevel, Scale, HORIZONTAL, Label, Button

prev_x = None
prev_y = None
canvas = None

selectedXFirst = None
selectedYFirst = None
selectedXSecond = None
selectedYSecond = None

selectRectangleId = None

#Standard variables
lineWidth = 2
backgroundColor = "white"
color = "black"


def drawingMode():
    '''Toggle drawing mode.'''
    deleteSelection()  # Delete any existing selection rectangle
    root.unbind("<Button-1>")
    root.unbind("<B1-Motion>")
    root.unbind("<ButtonRelease-1>")
    
    # root.bind("<Button-1>", onClickDraw) # Left mouse click
    root.bind("<B1-Motion>", onClickDraw) # Left mouse drag
    root.bind("<ButtonRelease-1>", onReleaseDraw) # Left mouse release
    
def selectMode():
    '''Toggle select mode.'''
    
    root.unbind("<Button-1>")
    root.unbind("<B1-Motion>")
    root.unbind("<ButtonRelease-1>")
    
    root.bind("<Button-1>", onClickSelect) # Left mouse click
    root.bind("<B1-Motion>", onDragSelect) # Left mouse drag
    root.bind("<ButtonRelease-1>", onReleaseSelect) # Left mouse release
    
def onClickDraw(event):
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

def onReleaseDraw(event):
    '''Handle mouse release events.'''
    global prev_x, prev_y
    # print("Mouse released at ({}, {})".format(event.x, event.y))
    prev_x, prev_y = None, None
    # REset the previous coordinates to prevent drawing lines when clicking after releasing the mouse button

def clear():
    '''Clear the canvas.'''
    drawingMode()
    global canvas, backgroundColor
    canvas.config(bg="white")  # Reset background color
    canvas.delete("all")
    # Delete all items from the canvas

        
def widthMenu():
    '''Open a dialog to select the line width.'''
    drawingMode()
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
    deleteSelection()  # Delete any existing selection rectangle
    drawingMode()
    global color
    selected_color = colorchooser.askcolor(title="Select Line Color")
    if selected_color[1] is not None:
        color = selected_color[1]
    
def backgroundMenu():
    '''Change the background color of the canvas.'''
    drawingMode()
    global canvas, backgroundColor
    selected_color = colorchooser.askcolor(title="Select Background Color")
    if selected_color[1] is not None:
        backgroundColor = selected_color[1]
    canvas.config(bg=backgroundColor)
    # Change the background color of the canvas
    
def eraser():
    '''Change the color to white to act as an eraser.'''
    drawingMode()
    global color
    color = "white"
    
def select():
    '''Select Area'''
    global selectRectangleId
    if selectRectangleId is not None:
        canvas.delete(selectRectangleId)
        selectRectangleId = None
    selectMode()

def onClickSelect(event):
    '''Handle mouse click events for selection.'''
    global selectedXFirst, selectedYFirst, selectRectangleId

    deleteSelection()  # Delete any existing selection rectangle
    
    selectedXFirst = event.x
    selectedYFirst = event.y 

def onDragSelect(event):
    '''Handle mouse drag events for selection.'''
    global selectedXSecond, selectedYSecond, selectRectangleId
    selectedXSecond = event.x
    selectedYSecond = event.y
    deleteSelection()  # Delete any existing selection rectangle
    selectRectangleId = canvas.create_rectangle(selectedXFirst, selectedYFirst, selectedXSecond, selectedYSecond, outline="red", width=2)

def onReleaseSelect(event):
    '''Handle mouse release events for selection.'''
    global selectedXSecond, selectedYSecond, selectRectangleId
    selectedXSecond = event.x
    selectedYSecond = event.y
    
    # Remove previous selection rectangle to avoid duplicates, which is leading to not deleting one of them
    deleteSelection()  # Delete any existing selection rectangle
    
    # Check if the selection rectangle is valid
    if selectedXFirst == selectedXSecond and selectedYFirst == selectedYSecond:
        return
    
    selectRectangleId = canvas.create_rectangle(selectedXFirst, selectedYFirst, selectedXSecond, selectedYSecond, outline="red", width=2)
    
    print("SelectId: %s" % selectRectangleId)

def draw():
    '''Set the mode to drawing.'''
    global selectRectangleId, color
    color = "black"  # Reset color to black for drawing
    drawingMode()

def deleteSelection():
    '''Delete the selected area.'''
    global selectRectangleId
    if selectRectangleId is not None:
        canvas.delete(selectRectangleId)
        selectRectangleId = None
    

root = Tk()
frm = ttk.Frame(root)
frm.grid(row = 0, column = 0, sticky = "NSEW")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#Buttons section
ttk.Button(frm, text="Clear", command=clear).grid(row=0, column=0, sticky="EW")
ttk.Button(frm, text="Width", command=widthMenu).grid(row=0, column=1, sticky="EW")
ttk.Button(frm, text="Eraser", command=eraser).grid(row=0, column=2, sticky="EW")
ttk.Button(frm, text="Pen", command=draw).grid(row=0, column=3, sticky="EW")
ttk.Button(frm, text="Color", command=colorMenu).grid(row=1, column=0, sticky="EW")
ttk.Button(frm, text="Background", command=backgroundMenu).grid(row=1, column=1, sticky="EW")
ttk.Button(frm, text="Select", command=select).grid(row=1, column=2, sticky="EW")

# Create a canvas for drawing with a white background
canvas = Canvas(frm, bg=backgroundColor)
canvas.grid(row=2, column=0, columnspan=99, sticky="NSEW")

# Configure the grid layout for the frame
frm.grid_rowconfigure(0, weight=0)
frm.grid_rowconfigure(1, weight=0)
frm.grid_rowconfigure(2, weight=1)

frm.grid_columnconfigure(0, weight=1)
frm.grid_columnconfigure(1, weight=1)
frm.grid_columnconfigure(2, weight=1)
frm.grid_columnconfigure(3, weight=1)

# Set the window to full screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("{}x{}".format(screen_width, screen_height))

drawingMode()  # Set the initial mode to drawing

root.mainloop()