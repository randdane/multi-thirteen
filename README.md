# multi-thirteen

This is a very small application I built to help kids learn their multiples from 1 to 13. It generates a random sequence of numbers from 2 to 13 which will be used to the multiply by numbers 1 through 13.

[screen shot](sample_image.png)

## Installation

Just go to a directory of your choice, clone the repo, and run `multi-thirteen.py`

```
$ git clone https://github.com/whiterd/multi-thirteen.git
```

## Instructions

Click the 'Start' button to begin the exercise and start the timer. The cursor will automatically set focus on the first textbox you should use. As you enter each answer, press Tab to move on to the next cell below. After all cells on the first page are filled in, press Enter to get the next set. This will be done for all set of multiples from 1 to 13. Once the last cell has been entered, the application will give you your time, reset the textboxes, and log the exercise in a SQLite3 database.

## Notes

* The contents of all textboxes are appended to a single list as integers and converted to an array. This is then stored in the database in binary fromat for maximum compression.
* The upper multiple, 13, is global and may be increased or made configurable in future iterations.
* Each entry row is dynamically generated based on the upper multiple.
```python
for index in range(self.MULTIPLE - 1):
   exec(f'self.text_{index}_1 = tkinter.StringVar()')
   exec(f'self.entry_{index}_1 = tkinter.Entry(self.window, textvariable=self.text_{index}_1, width=3)')
   exec(f'self.entry_{index}_1.grid(row={index}, column=1)')
```

## TODO

* Develop a format to return previous exercises back to the user.
