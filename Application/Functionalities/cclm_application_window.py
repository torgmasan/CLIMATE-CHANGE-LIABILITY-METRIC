from PyQt5.QtWidgets import QMainWindow


class CCLMApplicationWindow(QMainWindow):
    """An abstract class that provides the framework for each
    QWindow that is a part of the Climate Change Liability Metric project
    """

    def __init__(self):
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
