from ansidocs.src.classes.static.config import Config

class UknownLayoutException(Exception):
    """Exception raised when a project does not match a known layout

    Attributes:
        known_layouts     -- layouts that we do know about
        project_directory -- path to the project with unknown layout
    """

    def __init__(self, project_directory):
        self.known_layouts = Config.layouts()
        self.project_directory = project_directory
        super().__init__(f"Project at {project_directory} does not match any of the known layouts.")
