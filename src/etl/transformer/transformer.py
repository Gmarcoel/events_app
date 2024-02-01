class Transformer:
    def __init__(self, operations=None):
        """
        Initialize the Transformer with a list of operations.
        Each operation is a function that takes data as input and returns transformed data.
        """
        self.operations = operations if operations is not None else []

    def add_operation(self, operation):
        """
        Add a new operation to the transformation pipeline.
        """
        self.operations.append(operation)

    def transform(self, data):
        """
        Apply all the operations in sequence to the input data.
        """
        for operation in self.operations:
            data = operation(data)
        return data