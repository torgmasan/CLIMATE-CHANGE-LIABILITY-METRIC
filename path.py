import os


def _global_project_path(current_path: str) -> str:
    """Gives path of the root directory of project, irrespective
    of location from which the function is called.

    Preconditions:
        - Project file structure has not been tampered with
    """
    if os.path.split(current_path)[1] == 'CLIMATE-CHANGE-LIABILITY-METRIC':
        return current_path
    else:
        new_path = os.path.split(current_path)[0]
        return _global_project_path(new_path)


GLOBAL_PROJECT_PATH = _global_project_path(os.getcwd())
