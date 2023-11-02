class Solitaire():
    def __init__(self):
        pass

    def __repr__(self):
        return 'Solitaire'
    def __str__(self):
        return 'Solitaire'

    @classmethod
    def name(cls):
        """Return the name of the class as a string.
        Classmethod so it can be used without an instance
        """
        return 'BlackJack'