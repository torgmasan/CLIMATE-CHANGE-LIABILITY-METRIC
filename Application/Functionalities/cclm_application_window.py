"""
Parent script for CCLM GUI.
"""
from typing import Optional

from PyQt5.QtWidgets import QMainWindow


class CCLMApplicationWindow(QMainWindow):
    """An abstract class that provides the framework for each
    QWindow that is a part of the Climate Change Liability Metric project
    """
    next_win: Optional[QMainWindow] = None

    def __init__(self) -> None:
        super().__init__()

        self.next_win = None

    def populate_grid(self) -> None:
        """Adds widgets in a grid to the window"""
        raise NotImplementedError

    def next_window(self) -> None:
        """Provide functionality for the button responsible
        for window navigation
        """
        self.close()
        if self.next_win is not None:
            self.next_win.show()


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['math'],
        'max-line-length': 100,
        'disable': ['E0611', 'E9999']
    })
