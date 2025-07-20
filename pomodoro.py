import time
from tkinter import *
import sys
import os

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller bundled .exe.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
secondes=0
count =False
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset () :
    global secondes,timer
    my_manager.pomo_counter=1
    check_right.config(text="✔" * int(my_manager.pomo_counter / 2), background=YELLOW, fg=GREEN, font=(FONT_NAME, 12))
    my_manager.minutes=WORK_MIN
    secondes= 0
    my_canvas.itemconfig(time_text,text =f'{my_manager.minutes:02d}:{secondes:02d}')
    start_button.config(state="normal")
    if timer :
        my_screen.after_cancel(timer)

# ---------------------------- TIMER MECHANISM ------------------------------- #
class MinutesManager :
    def __init__(self):
        self.pomo_counter=1
        self.minutes = WORK_MIN
        self.current_period="Work"
    def next_periodd (self)  :
        self.pomo_counter+=1
        if self.pomo_counter%8==0 :
            self.minutes=LONG_BREAK_MIN
            self.current_period="Break"
        elif self.pomo_counter%2==0 :
            self.minutes=SHORT_BREAK_MIN
            self.current_period="Break"
        else:
            self.minutes=WORK_MIN
            self.current_period="Work"



# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def star_counter () :
    global count
    count= True
    start_button.config(state="disabled")
    count_down()

def count_down ():
    global secondes,timer

    if my_manager.minutes == 0 and secondes==0 :
        my_manager.next_periodd()
        check_right.config(text="✔"*int(my_manager.pomo_counter/2),background=YELLOW,fg=GREEN,font=(FONT_NAME,12))

        my_screen.after_cancel(timer)
        start_button.config(state="normal")
        my_canvas.itemconfig(time_text,text =f'{my_manager.minutes:02d}:{secondes:02d}')

        return
    if secondes == 0 :
        my_manager.minutes-=1
        secondes = 60

    secondes-=1
    minutes = my_manager.minutes

    my_canvas.itemconfig(time_text,text =f'{minutes:02d}:{secondes:02d}')



    timer=my_screen.after(1000,count_down)


# ---------------------------- UI SETUP ------------------------------- #
my_screen = Tk()
my_manager =MinutesManager()
my_screen.title("pomodoro App")
my_screen.config(padx=80,pady=40,background=YELLOW)

Time_label = Label(text="Timer" ,font=(FONT_NAME,38,"bold"),fg=GREEN,background=YELLOW)
Time_label.grid(column=1,row=0)
Time_label.config(padx=0)
my_canvas = Canvas(width=205,height=224,background=YELLOW,highlightthickness=0)
tomato_img_path = resource_path("tomato.png")
tomato = PhotoImage(file=tomato_img_path)
my_canvas.create_image(104,112,image=tomato)
my_canvas.grid(row=1,column=1)
time_text =my_canvas.create_text(112,130,text=f'25:00',fill="white",font=(FONT_NAME,28,"bold"))
start_button = Button( text="Start",
    command=star_counter,
    bg="#4CAF50",        # background color
    fg="white",          # text color
    activebackground="#45a049",
    font=("Arial", 12, "bold"),
    relief="raised",     # border style
    bd=4,                # border width
    padx=10, pady=5    )
start_button.grid(column=0,row=2)

Reset_button = Button( text="Reset",
    command=reset,
    bg="#4CAF50",        # background color
    fg="white",          # text color
    activebackground="#45a049",
    font=("Arial", 12, "bold"),
    relief="raised",     # border style
    bd=4,                # border width
    padx=10, pady=5    )
Reset_button.grid(column=3,row=2)


check_right =Label(text="",background=YELLOW,fg=GREEN,font=(FONT_NAME,12))
check_right.grid(column=1,row=3)






my_screen.mainloop()
