import sys
from random import SystemRandom
from tkinter import scrolledtext
from tkinter import *

try:
    import Queue as qu
    import Tkinter as tk
except ImportError:
    import queue as qu
    import tkinter as tk


class TeeStd(object):
    def __init__(self, queue, type, name, mode):

        self.queue = queue
        self.file = open(name, mode)
        if type == 'stderr':
            self.out_obj = sys.stderr
            sys.stderr = self
        else:
            self.out_obj = sys.stdout
            sys.stdout = self

    def write(self, data):
        self.queue.put(data)

APP_WIN_XPOS = 50
APP_WIN_YPOS = 50

class App(object):
    def __init__(self):
        self.win = tk.Tk()
        self.win.geometry('+{0}+{1}'.format(APP_WIN_XPOS, APP_WIN_YPOS))
        self.win.protocol("WM_DELETE_WINDOW", self.close)

        self.queue = qu.Queue()

        self.text = tk.Text(self.win, width=95, height=20, highlightthickness=0, bd=0, fg='light green', bg='black', font="Verdana 10 bold", relief='sunken',
                            padx=1, pady=1)
        self.text = scrolledtext.ScrolledText(self.win, width=95, height=20, fg='light green', bg='black', font="Verdana 10 bold")
        self.text.pack()

        generate_button = tk.Button(self.win, text='generate SEED',
                                    command=self.generate_trigger)
        generate_button.pack(side='left')

        exit_button = tk.Button(self.win, text='Exit',
                                command=self.exit_trigger)
        exit_button.pack(side='right')

        self.sampler()

### --- METHODEN --- ###

    def generate_trigger(self):
        alphabet = '9ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        generator = SystemRandom()
        print("")
        print(''.join(generator.choice(alphabet) for _ in range(81)))
        print("")

    def exit_trigger(self):
        command = self.win.destroy()

    def sampler(self):

        if self.queue.qsize():
            try:
                data = self.queue.get()
                self.text.insert('end', data)
                self.queue.task_done()
            except qu.Empty:
                pass

        self.win.after(50, self.sampler)

    def run(self):
        self.win.mainloop()

    def close(self):
        self.win.destroy()

### --- METHODEN END --- ###

### --- AUFRUF --- ###
app = App()
app.win.title(">>IOTA<< Seed-Generator")

TeeStd(app.queue, 'stderr', "log.txt", "a");
TeeStd(app.queue, 'stdout', "log.txt", "a")

print(" >>IOTA<<  SEED-Generator (81 Zeichen + die Zahl 9, zufällige Reihenfolge)")
print("-------------------------------------------------------------------------------")

app.run()
