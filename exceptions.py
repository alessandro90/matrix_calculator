class CalculatorError(Exception):
    """
    Base class. All the exceptions of the application
    inherit from this base.
    """
    def __init__(self, msg):
        super().__init__(msg)

class FormatError(CalculatorError):
    """
    Raised if invalid text in written in
    the Text widgets reserved for the matrices.
    """
    def __init__(self, msg = "Format Error."):
        super().__init__(msg)

class EmptyMatrixError(CalculatorError):
    """
    Raised if a required matrix for the computation
    is missing.
    """
    def __init__(self, msg = "Missing required matrix."):
        super().__init__(msg)

class NonComputableError(CalculatorError):
    """
    Raised if the computation is not feasible, e.g.
    the result does not converge.
    """
    def __init__(self, msg = "Wrong format or\nresult does not converge."):
        super().__init__(msg)
