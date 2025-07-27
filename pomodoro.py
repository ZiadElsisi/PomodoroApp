import time
from tkinter import *
import sys
import os
import pygame
pygame.mixer.init()
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
seconds=0
count =False
timer = None


# ---------------------------- TIMER sound ------------------------------- #
tickpath=resource_path("clock-ticking.wav")
alarmpath = resource_path("the_best_alarm.mp3")
ticksound=pygame.mixer.Sound(tickpath)
alarm_Sound = pygame.mixer.Sound(alarmpath)
def mute_sound() :
    if ticksound.get_volume() ==0.0 :
        ticksound.set_volume(1.0)
        mute_button.config(text="mute",bg="#fc4903",activebackground="#c95b16")
    else:
        ticksound.set_volume(0.0)
        mute_button.config(text="unmute", bg="#4CAF50",activebackground="#45a049")


# ---------------------------- TIMER RESET ------------------------------- #
def reset () :
    global seconds,timer
    alarm_Sound.set_volume(0.0)

    my_manager.pomo_counter=1
    check_right.config(text="✔" * int(my_manager.pomo_counter / 2), background=YELLOW, fg=GREEN, font=(FONT_NAME, 12))
    Time_label.config(text=f'timer', fg=GREEN)
    my_manager.current_period = "Work"

    my_manager.minutes=WORK_MIN
    seconds= 0
    my_canvas.itemconfig(time_text,text =f'{my_manager.minutes:02d}:{seconds:02d}')
    start_button.config(state="normal")
    if timer :
        my_screen.after_cancel(timer)

# ---------------------------- TIMER MECHANISM ------------------------------- #
class MinutesManager :
    def __init__(self):
        self.pomo_counter=1
        self.minutes = WORK_MIN
        self.current_period="Work"
    def next_period (self)  :
        self.pomo_counter+=1
        if self.pomo_counter%8==0 :
            self.minutes=LONG_BREAK_MIN
            self.current_period="Break"
            Time_label.config(text=f'{self.current_period}',fg=RED)
        elif self.pomo_counter%2==0 :
            self.minutes=SHORT_BREAK_MIN
            self.current_period="Break"
            Time_label.config(text=f'{self.current_period}',fg=PINK)

        else:
            self.minutes=WORK_MIN
            self.current_period="Work"
            Time_label.config(text=f'{self.current_period}',fg=GREEN)
        alarm_Sound.set_volume(1.0)
        alarm_Sound.play(maxtime=8000)
        print("nnananana")


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def start_counter () :
    global count
    alarm_Sound.set_volume(0.0)
    count= True
    start_button.config(state="disabled")
    count_down()

def count_down ():
    global seconds,timer
    if my_manager.pomo_counter==1 :
        Time_label.config(text=f'{my_manager.current_period}', fg=GREEN)

    if my_manager.minutes == 0 and seconds==0 :
        my_manager.next_period()
        check_right.config(text="✔"*int(my_manager.pomo_counter/2),background=YELLOW,fg=GREEN,font=(FONT_NAME,12))

        my_screen.after_cancel(timer)
        start_button.config(state="normal")
        my_canvas.itemconfig(time_text,text =f'{my_manager.minutes:02d}:{seconds:02d}')

        return
    if seconds == 0 :
        my_manager.minutes-=1
        seconds = 60
    if not pygame.mixer.get_busy():
            ticksound.play(maxtime=100)
    seconds-=1
    minutes = my_manager.minutes

    my_canvas.itemconfig(time_text,text =f'{minutes:02d}:{seconds:02d}')



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
start_button = Button( text="▶ Start",
    command=start_counter,
                       bg="#4CAF50",  # background color
                       fg="white",  # text color
                       activebackground="#45a049",
                       font=("Arial", 12, "bold"),
                       relief="raised",  # border style
                       bd=4,  # border width
                       padx=10, pady=5
                       )
start_button.grid(column=0,row=2)

Reset_button = Button( text="⟳ Reset",
    command=reset,
    bg="#4CAF50",        # background color
    fg="white",          # text color
    activebackground="#45a049",
    font=("Arial", 12, "bold"),
    relief="raised",     # border style
    bd=4,                # border width
    padx=10, pady=5    )
Reset_button.grid(column=3,row=2)

mute_button = Button( text="mute", width=8,
    command=mute_sound,
    bg="#fc4903",        # background color
    fg="white",          # text color
    activebackground="#c95b16",
    font=("Arial", 9, "bold"),
    # relief="raised",     # border style
    # bd=4,                # border width
    padx=0, pady=5    )
mute_button.place(x=-60,y=-25)


check_right =Label(text="",background=YELLOW,fg=GREEN,font=(FONT_NAME,12))
check_right.grid(column=1,row=3)



my_screen.mainloop()

