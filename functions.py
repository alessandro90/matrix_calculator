from collections import defaultdict
import numbers
import numpy as np
from tkinter import *
from exceptions import *


def make_computation(operations, op, header, matrix_frames):
    """
    Function binded to the menu options.
    It configures the 'Compute' button with the function
    'compute_op'.
    Parameters:
    operations: operations dictionary;
    op: requested operation;
    header: the header widget ('Compute' button plus 'Digits');
    matrix_frames: all the matrix widgets.
    """
    def inner():
        matrix_frames.Result.text_box.delete("1.0", END)
        matrix_frames.Result.label.configure(text = op)
        header.compute.configure(command = compute_op(operations, op, 
            matrix_frames, header))
    return inner


def compute_op(operations, op, matrix_frames, header):
    """
    Retrieve the input from the Text widgets.
    Calls 'convert_to_matrix' to retrieve a list of
    numeric matrices.
    Calls 'produce_result' which actually computes the
    requested operation.
    Finally, calls 'display_result' which print on
    screen the result.
    Parameters:
    operations: operations dictionary;
    op: requested operation;
    matrix_frames: all the matrix widgets;
    header: the header widget ('Compute' button plus 'Digits').
    """
    def inner():
        matrices = []
        for matrix in matrix_frames:
            matrices.append(matrix.text_box.get("1.0", "end-1c"))
        try:
            operands = convert_to_matrix(matrices, operations, op)
        except CalculatorError as e:
            result = e
        else:
            np_mats = []
            for matrix in operands.values():
                np_mats.append(np.array(matrix))
            try:
                result = produce_result(op, np_mats)
            except CalculatorError as e:
                result = e
        finally:
            display_result(result, matrix_frames, header)
    return inner    


def convert_to_matrix(matrices, operations, op):
    """
    Converts the Text widgets into numeric matrices.
    Parameters:
    matrices: list of text input matrices;
    operations: operations dictionary;
    op: requested operation.
    Returns:
    input_mats: list of numeric input matrices.
    Raises:
    EmptyMatrixError if a missing matrix is detected.
    FormatError if invalid text is inserted.
    """
    input_mats = defaultdict(list)
    for matrix_index, mat in enumerate(matrices[:operations[op]]):
        if not mat:
            raise EmptyMatrixError
        rows = mat.split('\n')
        for row in rows:
            row = row.replace('\t', ' ')
            if row.count(' ', 0, len(row)) != len(row):
                numeric_row = []
                elements = row.split(' ')
                for element in elements:
                    if element:
                        try:
                            if 'j' in element:
                                el = complex(element)
                                if el == complex(0):
                                    numeric_row.append(0)
                                else:
                                    numeric_row.append(el)
                            else:
                                numeric_row.append(float(element))
                        except ValueError:
                            raise FormatError
                input_mats[matrix_index].append(numeric_row)
    return input_mats


def produce_result(op, np_mats):
    """
    Compute the requested operation.
    Parameters:
    op: requested operation;
    np_mats: list of input numeric matrices.
    Returns:
    Computed result.
    Raises:
    FormatError or NotComputableError.
    """
    if op == "Sum":
        try:
            result = sum(np_mats)
        except (TypeError, ValueError) as e:
            raise FormatError
    elif op == "Multiplication":
        try:
            result = np_mats[0].dot(np_mats[1])
        except (TypeError, ValueError):
            raise FormatError
    elif op == "Determinant":
        try:
            result = np.linalg.det(np_mats[0])
        except np.linalg.linalg.LinAlgError:
            raise FormatError
    elif op == "Eigenvalues":
        try:
            result = np.linalg.eigvals(np_mats[0])
        except np.linalg.LinAlgError:
            raise NonComputableError
    elif op == "Eigenvectors":
        try:
            _, result = np.linalg.eig(np_mats[0])
        except np.linalg.LinAlgError:
             NonComputableError
    elif op == "Singular values":
        try:
            _, result, _ = np.linalg.svd(np_mats[0])
        except:
            raise NonComputableError
    elif op == "Inversion":
        try:
            result = np.linalg.inv(np_mats[0])
        except np.linalg.LinAlgError:
            raise NonComputableError
    elif op == "Pseudo-inverse":
        try:
            result = np.linalg.pinv(np_mats[0])
        except np.linalg.LinAlgError:
            raise NonComputableError
    return result


def display_result(result, matrix_frames, header):
    """
    Display the result into the 'Result' widget,
    rounded with the requested digits.
    Parameters:
    result: numeric result;
    matrix_frames: all the matrix widgets;
    header: 'Compute' button plus 'Digits' widgets.
    """
    digits = header.get_decimal_digits()
    matrix_frames.Result.text_box.delete("1.0", END)
    str_result = ''
    if type(result) == np.ndarray:
        for row in result:
            try:
                for element in row:
                    str_result += str(round(element, digits)) + ' '
            except TypeError:
                str_result += str(round(row, digits)) + '\n'
            else:
                str_result += '\n'
    else:
        if isinstance(result, numbers.Number):
            str_result = str(round(result, digits))
        else:
            str_result = str(result)
    matrix_frames.Result.text_box.insert(END, str_result)
