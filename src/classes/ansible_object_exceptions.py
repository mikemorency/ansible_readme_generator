
class AnsibleMetadataError(Exception):
    def __init__(self, root_dir: str, attribute_error: AttributeError):
        self.root_dir = root_dir
        self.attribute_error = attribute_error
        self.message = f"{attribute_error}, add this attribute to the meta.yml or galaxy.yml"
        super().__init__(self.message)

class MissingVariableDescription(Exception):
    def __init__(self, missing_variables: set):
        self.missing_variables = missing_variables
        self.message = f"The following variables are missing descriptions: {missing_variables}"
        super().__init__(self.message)
