from os import path
from dataclasses import dataclass
import yaml
import logging

from ansidocs.src.classes.abstract_project_part import AbstractProjectPart
from ansidocs.src.classes.abstract_project_part import AbstractDirContent
from ansidocs.src.classes.layout import Layout


logger = logging.getLogger(__name__)


@dataclass
class DefaultsDirContent(AbstractDirContent):
    """Class for keeping track of stuff in a plugin directory."""
    default_parameters: list


@dataclass
class DefaultParameter():
    """Class for keeping track of stuff in a plugin directory."""
    name: str
    value: object
    description: str
    required: bool


class Defaults(AbstractProjectPart):
    def __init__(self, project_root: str, layout: Layout):
        super().__init__(layout=layout, project_root=project_root)
        self.root_dir = path.abspath(path.join(self.project_root, layout.part_paths['defaults']))
        if not path.exists(self.root_dir):
            raise FileNotFoundError(f"Unable to find defaults project part directory {self.root_dir}")

    def get_values(self):
        with open(path.join(self.root_dir, "main.yml")) as f:
            defaults = yaml.safe_load(f)

        return defaults

    def get_descriptions(self):
        defaults_desc_file = path.join(self.project_root, self.layout.docs, "defaults.yml")
        try:
            with open(defaults_desc_file) as f:
                descr = yaml.safe_load(f)
        except FileNotFoundError:
            logger.critical(f"No defaults description file found at {defaults_desc_file}. "
                            "This file is required when defaults are present")
            raise
        return descr

    def get_content(self):
        content = []
        values = self.get_values()
        if values:
            descr  = self.get_descriptions()

            for k, v in values.items():
                content += [DefaultParameter(
                    name=k,
                    value=v,
                    required=bool(v == ''),
                    description=descr.get(k, None)
                )]

        return DefaultsDirContent(subdirs=[], default_parameters=content)

    def to_markdown(self):
        markdown =  [ "### Variables", ""]
        content = self.get_content()

        if content.default_parameters:
            markdown += ["The following table contains variables you can override and their default values:"]
            markdown += ["<table>", "<tr>", "<th>Variable Name</th>", "<th>Required</th>"]
            markdown += ["<th>Default Value</th>", "<th>Description</th>", "</tr>"]
            for parameter in content.default_parameters:
                markdown += ["<tr>"]
                markdown += [
                    f"<th>{parameter.name}</th>",
                    f"<th>{parameter.required}</th>",
                    f"<th>{parameter.value}</th>",
                    f"<th>{parameter.description}</th>"
                ]
                markdown += ["</tr>"]
            markdown += ["</table>"]
        else:
            markdown += ["There are no input parameters availble for this project."]

        return markdown
