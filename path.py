"""
Provides a universal path in order to avoid using
relative path. This prevents errors when bridging
the user interaction scripts with the computation scripts.
"""

import os


def _global_project_path(current_path: str) -> str:
    """Gives path of the root directory of project, irrespective
    of location from which the function is called.

    Preconditions:
        - Project file structure has not been tampered with
        - File was downloaded as per instructions from github
        or markus
    """
    markus_root = 'CFRCC'
    github_root = 'CLIMATE-CHANGE-LIABILITY-METRIC'

    if os.path.split(current_path)[1] in {markus_root, github_root}:
        return current_path

    return _global_project_path(os.path.split(current_path)[0])


GLOBAL_PROJECT_PATH = _global_project_path(os.getcwd())


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['math'],
        'max-line-length': 100,
        'disable': ['E9999']
    })
