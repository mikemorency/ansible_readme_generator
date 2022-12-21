from os import path
from os import strerror
from dataclasses import dataclass
import yaml
import logging
import errno

from ansidocs.classes.abstract_project_part import AbstractProjectPart
from ansidocs.classes.abstract_project_part import AbstractDirContent
from ansidocs.classes.exceptions import DefaultParamMissingDescription
from ansidocs.classes.layout import Layout


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
        self.defaults_desc_file = path.join(self.project_root, self.layout.docs, "defaults.yml")
        if not path.exists(self.root_dir):
            raise FileNotFoundError(
                errno.ENOENT,
                f"Unable to find defaults project part directory {self.root_dir}",
                self.root_dir)

    def get_values(self):
        try:
            with open(path.join(self.root_dir, "main.yml")) as f:
                values = yaml.safe_load(f)
                return {} if values is None else values
        except FileNotFoundError:
            return {}

    def get_descriptions(self):
        try:
            with open(self.defaults_desc_file) as f:
                descr = yaml.safe_load(f)
                return {} if descr is None else descr
        except FileNotFoundError:
            return {}

    def get_content(self):
        content = []
        values = self.get_values()
        descr = self.get_descriptions()

        if values and not descr:
            logger.critical(f"No defaults description file found at {self.defaults_desc_file}. "
                            "This file is required when defaults are present")
            raise FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), self.defaults_desc_file)

        for key in sorted(set(list(values.keys()) + list(descr.keys()))):
            try:
                default_desc = descr[key]
            except KeyError:
                raise DefaultParamMissingDescription(name=key, docs_dir=self.defaults_desc_file)

            try:
                default_val = values[key]
                required = False
            except KeyError:
                logger.info("Default key {key} has a documented description "
                            "but is missing a value. Marking as required")
                default_val = None
                required = True

            content += [DefaultParameter(
                name=key,
                value=default_val,
                required=required,
                description=default_desc
            )]

        return DefaultsDirContent(subdirs=[], default_parameters=content)

    def to_markdown(self):
        markdown = ["### Variables", ""]
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
