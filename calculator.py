from collections import namedtuple, OrderedDict
import tkinter as tk
from frames import *
from functions import *


operations = OrderedDict({"Sum": 2, 
                          "Multiplication": 2, 
                          "Determinant": 1, 
                          "Eigenvalues": 1,
                          "Eigenvectors": 1,
                          "Singular values": 1,
                          "Inversion": 1,
                          "Pseudo-inverse": 1})

root = MyRoot(3, 2)
root.title("Matrix Calculator")

matrix1 = MyFrame(root, name = "Matrix 1", row = 1, column = 0)
matrix2 = MyFrame(root, name = "Matrix 2", row = 1, column = 1)
result = MyFrame(root, name = "Result", row = 2, columnspan = 2)

AllFrames = namedtuple('AllFrames', ('matrix1', 'matrix2', 'Result'))
matrix_frames = AllFrames(matrix1, matrix2, result)


header = Header(root, matrix_frames)

menu = tk.Menu(root)
available_ops = tk.Menu(menu)
menu.add_cascade(label = "Operations", menu = available_ops)
for operation in operations.keys():
    available_ops.add_command(label = operation, command = 
        make_computation(operations, operation, header, matrix_frames))

root.config(menu = menu)
root.mainloop()
