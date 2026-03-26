class InvalidInput(Exception):
    """Raised when the input provided to a function is invalid."""

    def init(self, message="Invalid input provided."):
        self.message = message
        super().init(self.message)
        
class IlligalMove(Exception):
    '''Raised when illigal move is made.'''

    def init(self, message="Illigal move made."):
        self.message = message
        super().init(self.message)