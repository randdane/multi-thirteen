from datetime import datetime
from random import shuffle
import tkinter
from tkinter import messagebox
from backend import Database

database = Database('multi-13-runs.db')


class Interface:
    """tk interface for Multi-13."""

    def __init__(self):
        self.time_start = None
        self.time_stop = None
        self.RECORDS = []  # Collect data from each completed row.
        self.MULTIPLE = 13  # Highest multiple to use.
        self.CURRENT = 1

        self.window = tkinter.Tk()
        self.window.wm_title("Multi-Thirteen")

        self.menu_bar = tkinter.Menu(self.window)
        self.file_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label='Records', accelerator='Ctrl+O', command=self.cmd_see_records)
        self.file_menu.add_command(label='Quit', accelerator='Ctrl+Q', command=self.window.destroy)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.help_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.cmd_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.window.config(menu=self.menu_bar)
        self.window.bind("<Control-o>", self.cmd_see_records)
        self.window.bind("<Control-q>", self.cmd_quit)
        self.window.bind('<Return>', func=self.cmd_next)

        btn_gen = tkinter.Button(self.window, text="Start", width=12, command=self.cmd_start)
        btn_gen.grid(row=0, column=0, rowspan=2, sticky=tkinter.N, padx=5, pady=5)

        # Generate each row for numbers 2 through 13 (if 13 is to be the highest for this example).
        for index in range(self.MULTIPLE - 1):
            exec(f'self.text_{index}_1 = tkinter.StringVar()')
            exec(f'self.entry_{index}_1 = tkinter.Entry(self.window, textvariable=self.text_{index}_1, width=3)')
            exec(f'self.entry_{index}_1.grid(row={index}, column=1)')

            lbl_x = tkinter.Label(self.window, text=' x ')
            lbl_x.grid(row=index, column=2)

            exec(f'self.text_{index}_3 = tkinter.StringVar()')
            exec(f'self.entry_{index}_3 = tkinter.Entry(self.window, textvariable=self.text_{index}_3, width=3)')
            exec(f'self.entry_{index}_3.grid(row={index}, column=3)')

            lbl_eq = tkinter.Label(self.window, text=' = ')
            lbl_eq.grid(row=index, column=4)

            exec(f'self.text_{index}_5 = tkinter.StringVar()')
            exec(f'self.entry_{index}_5 = tkinter.Entry(self.window, textvariable=self.text_{index}_5, width=7)')
            exec(f'self.entry_{index}_5.grid(row={index}, column=5, sticky=tkinter.W, padx=6, pady=5)')

        #self.window.geometry('255x270')
        self.window.mainloop()

    def __del__(self):
        print(self.RECORDS)

    def cmd_see_records(self, *args):
        """Display previously recorded exercise times.
        *args needed to handle event object being sent due to binding key(s).
        """
        messagebox.showinfo(message='Not yet implemented.', title='Records')

    def cmd_quit(self, *args):
        """Quit program by destroying window.
        *args needed to handle event object being sent due to binding key(s).
        """
        self.window.destroy()

    def cmd_about(self):
        """Display popup with info about this program."""
        messagebox.showinfo(message='Created by Randall White', title='About')

    def cmd_start(self):
        """Populate numbers to be multiplied."""
        self.CURRENT = 1
        # Generate numbers to be used in exercise.
        numbers = [x for x in range(2, self.MULTIPLE + 1)]
        shuffle(numbers)

        # Distribute numbers to text boxes.
        for index, number in enumerate(numbers):
            exec(f'self.entry_{index}_1.insert(tkinter.END, {number})')
            exec(f'self.entry_{index}_1.config(state=tkinter.DISABLED)')  # Make unselectable.
            exec(f'self.entry_{index}_3.insert(tkinter.END, "1")')
            exec(f'self.entry_{index}_3.config(state=tkinter.DISABLED)')

        self.entry_0_5.focus_set()  # First row of last column (first user guess).

        # Start timer for user.
        self.time_start = datetime.now()

    def cmd_next(self, *args):
        """Record table, clear, and populate with next round of numbers.
        *args needed due to callback sent from binding the <Enter> key.
        """
        self.CURRENT += 1

        if self.CURRENT > self.MULTIPLE:
            self.end_exercise()
            return None

        for index in range(self.MULTIPLE - 1):
            num_random = eval(f'self.entry_{index}_1')
            num_multiple = eval(f'self.entry_{index}_3')
            num_guess = eval(f'self.entry_{index}_5')
            num_answer = str(int(num_random.get()) * int(num_multiple.get()))

            records = Interface.convert_to_int(num_random.get(),
                                               num_multiple.get(),
                                               num_guess.get(),
                                               num_answer)
            for number in records:
                self.RECORDS.append(number)

            num_multiple.config(state=tkinter.NORMAL)  # Re-enable to allow deletion.
            num_multiple.delete(0, tkinter.END)
            num_guess.delete(0, tkinter.END)
            num_multiple.insert(tkinter.END, self.CURRENT)
            num_multiple.config(state=tkinter.DISABLED)

            self.entry_0_5.focus_set()  # First row of last column.

    def end_exercise(self):
        """Save data and clear content."""
        self.time_stop = datetime.now()
        elapsed_time = str(self.time_stop - self.time_start)[2:7]  # Grab only minutes and seconds (e.g. 12:34)
        messagebox.showinfo(message='Completed in (minutes:seconds):',
                            detail=elapsed_time,
                            title='About')
        database.insert(self.time_start, elapsed_time, self.RECORDS)
        print('Data saved.')
        # Reset object.
        self.time_start = None
        self.time_stop = None
        self.RECORDS = []
        self.CURRENT = 1
        # Clear all fields.
        for index in range(self.MULTIPLE - 1):
            num_random = eval(f'self.entry_{index}_1')
            num_multiple = eval(f'self.entry_{index}_3')
            num_guess = eval(f'self.entry_{index}_5')
            num_random.config(state=tkinter.NORMAL)
            num_random.delete(0, tkinter.END)
            num_multiple.config(state=tkinter.NORMAL)
            num_multiple.delete(0, tkinter.END)
            num_guess.delete(0, tkinter.END)

    @staticmethod
    def convert_to_int(*args):
        """String to int, else 0.

        Input: '2', '3', '', '6'
        Output: 2, 3, 0, 6
        """
        converted = []
        for item in args:
            try:
                converted.append(int(item))
            except ValueError:
                converted.append(0)
        return converted


if __name__ == '__main__':
    multi_13 = Interface()
