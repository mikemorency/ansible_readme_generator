from ansidocs.classes.static.config import Config


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


class DefaultParamMissingDescription(Exception):
    """Exception raised when a default parameter does not have a documented description

    Attributes:
        name     -- The name of the default parameter in question
        docs_dir -- Directory that was searched for the description documentation file
    """

    def __init__(self, name: str, docs_dir: str):
        self.name = name
        self.docs_dir = docs_dir
        super().__init__(f"Default parameter {name} does not have a documented description.")
