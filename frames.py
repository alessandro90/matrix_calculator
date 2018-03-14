from tkinter import *

class MyRoot(Tk):
    """
    Class derived from tkinter.Tk.
    Sets and configures the row and columns
    of the main widget.
    """
    def __init__(self, rows, cols):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.configure()

    def configure(self):
        """
        Configure the main widget. Make it resizable.
        """
        for c in range(self.cols):
            self.columnconfigure(c, weight = 1)
        for r in range(self.rows):
            if r == 0:
                weight = 0
            else:
                weight = 1
            self.rowconfigure(r, weight = weight)


class Header(Frame):
    """
    Header widget (inherits from tkinter.Frame). Sets and configures
    the 'Compute' button and the 'digits'-related widgets.
    Methods:
    get_decimal_digits(self)
    Returns current number of digits in the 'digits' widget.
    If the result is invalid, it sets the number to 3.
    """
    def __init__(self, root, matrix_frames):
        super().__init__(root)
        self.grid(row = 0, columnspan = 2, sticky = N)
        self.configure()
        self.build_contents(matrix_frames)

    def configure(self):
        """
        Execute row- and columnconfigure commands.
        """
        self.columnconfigure(0, weight = 0)
        self.columnconfigure(1, weight = 0)
        self.columnconfigure(2, weight = 0)

    def build_contents(self, matrix_frames):
        """
        Set 'Compute' and 'Digits' widgets.
        """
        def warning():
            matrix_frames.Result.text_box.delete("1.0", END)
            matrix_frames.Result.text_box.insert(END, "Choose an operation.")

        self.compute = Button(self, text = "Compute", 
                 command = warning, font = 15)
        self.compute.grid(row = 0, column = 0)
        self.digits = Spinbox(self, from_ = 1, to = 20, width = 2, 
            textvariable = self.set_default_digits(), font = 12)
        self.digits.grid(row = 0, column = 1, padx = (15, 5))
        self.digits_label = Label(self, text = "Digits", font = 12)
        self.digits_label.grid(row = 0, column = 2)

    def set_default_digits(self):
        """Set the default digits number."""
        default = StringVar(self)
        default.set("3")
        return default

    def get_decimal_digits(self):
        """Get the current value of digits."""
        try:
            digits = int(self.digits.get())
            if digits < 0:
                raise ValueError("Negative digits are not allowed.")
        except ValueError:
            digits = 3
            self.digits.config(textvariable = self.set_default_digits())
        return digits


class MyFrame(Frame):
    """
    Frame class (inherits from tkinter.Frame) to manage the 'Matrix'-widgets.
    It is responsible for the labels, text areas and scrollbars.
    It has a __str__ method which returns the name of the widget.
    """
    width = 20
    height = 7
    def __init__(self, root, name = '', row = 0, column = 0, columnspan = None):
        super().__init__(root)
        self.name = name
        self.row = row
        self.column = column
        self.columnspan = columnspan
        self.grid_my_frame()
        self.configure()
        self.build_contents()

    def grid_my_frame(self):
        """Grid the frame."""
        if self.columnspan is None:
            self.grid(row = self.row, column = self.column, 
                sticky = N+S+E+W, padx = 15, pady = 5)
        else:
            self.grid(row = self.row, columnspan = self.columnspan, 
                sticky = N+S+E+W, padx = 100, pady = (5, 15))

    def configure(self):
        """Configure row 1 and column 0."""
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)

    def build_contents(self):
        """
        Build the Label, Text and Scrollbar widgets.
        Grid and configure all the widgets.
        """
        self.label = Label(self, text = self.name, font = 15)
        self.make_scrollbars()
        self.grid_scrollbars()
        self.text_box = Text(self, width = MyFrame.width, 
            height = MyFrame.height, wrap = NONE, relief = SUNKEN, 
            yscrollcommand = self.yscrollbar.set, xscrollcommand = self.xscrollbar.set)
        self.configure_scrollbars()
        self.label.grid(row = 0, column = 0, sticky = N+S+W+E)
        self.text_box.grid(row = 1, column = 0, sticky = N+S+W+E)

    def make_scrollbars(self):
        """Make the scrollbars."""
        self.xscrollbar = Scrollbar(self, orient = HORIZONTAL)
        self.yscrollbar = Scrollbar(self, orient = VERTICAL)

    def grid_scrollbars(self):
        """Grid the scrollbars."""
        self.yscrollbar.grid(column = 1, row = 1, sticky = N+S)
        self.xscrollbar.grid(column = 0, row = 2, sticky = E+W)

    def configure_scrollbars(self):
        """Configure the scrollbars."""
        self.xscrollbar.config(command = self.text_box.xview)
        self.yscrollbar.config(command = self.text_box.yview)

    def __str__(self):
        """Return the name of the widget."""
        return self.name
