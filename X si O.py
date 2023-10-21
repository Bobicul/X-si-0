from tkinter import *
from tkinter import messagebox
import time
import random

tk = Tk()
app_running = True  # Aflăm dacă aplicația este în funcțiune sau nu

size_canvas_x = 768
size_canvas_y = 768

def on_closing():
    global app_running
    if messagebox.askokcancel("Ieșire din joc", "Doriți să ieșiti din joc ?"):
        app_running = False
        tk.destroy()


tk.protocol("WM_DELETE_WINDOW", on_closing)

tk.title("Joc X și 0")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=size_canvas_x, height=size_canvas_y, bd=0, highlightthickness=0)
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white")
canvas.pack()
tk.update()


s_x = 3
s_y = s_x
step_x = size_canvas_x // s_x
step_y = size_canvas_y // s_y

def draw_table():
    for i in range(0, s_x + 1):
        canvas.create_line(0, i * step_y, size_canvas_x, i * step_y)
    for i in range(0, s_y + 1):
        canvas.create_line(i * step_y, 0, i * step_y, size_canvas_y)


points = [[-1 for i in range(s_x)] for i in range(s_x)]
list_ids = []
draw_table()

class Point:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

def draw_point(x, y, type):
    size = 25
    color = "black"
    id = 0
    if type == 0:
        color = "red"
        line_width = 0
        id = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color,width=line_width)
        id2 = canvas.create_oval(x * step_x + size, y * step_y + size, x * step_x + step_x - size, y * step_y + step_y - size, fill="white",width=line_width)
        list_ids.append(id)
        list_ids.append(id2)
    if type == 1:
        color = "blue"
        line_width = 30
        id = canvas.create_line(x * step_x + size, y * step_y + size, x * step_x + step_x - size, y * step_y + step_y - size, fill=color, width=line_width)
        id2 = canvas.create_line(x * step_x + size, y * step_y + step_y - size, x * step_x + step_x - size, y * step_y + size, fill=color, width=line_width)
        list_ids.append(id)
        list_ids.append(id2)

def add_to_points(event):
    global points
    type = 0
    if event.num == 3:
        type = 1
    if points[event.x // step_x][event.y // step_y] == -1:
        points[event.x // step_x][event.y // step_y] = type
        draw_point(event.x // step_x, event.y // step_y, type)
        if check_winner(type):
            winner = "roșu" if type == 0 else "albastru"
            show_winner(winner)
            points = [[10 for i in range(s_x)] for i in range(s_x)]

canvas.bind_all("<Button-1>", add_to_points)  # LMB
canvas.bind_all("<Button-3>", add_to_points)  # RMB

def button_press():
    global list_ids
    global points
    for i in list_ids:
        canvas.delete(i)
    list_ids = []
    points = [[-1 for i in range(s_x)] for i in range(s_x)]

b1 = Button(tk, text="Încercați din nou!", command=button_press)
b1.pack()

def check_winner(who):
    for j in range(0, s_y):
        win = True
        for i in range(0, s_x):
            if points[j][i] != who:
                win = False
        if win:
            return True
    for j in range(0, s_y):
        win = True
        for i in range(0, s_x):
            if points[i][j] != who:
                win = False
        if win:
            return True

    win = True
    for i in range(0, s_y):
        if points[i][i] != who:
            win = False
    if win:
        return True

def show_winner(winner):
    messagebox.showinfo("Câștigătorul", f"Câștigătorul este {winner}!")

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)

tk.mainloop()
