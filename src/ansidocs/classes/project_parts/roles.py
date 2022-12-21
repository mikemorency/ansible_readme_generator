from os import path
import logging
from dataclasses import dataclass
import glob
import errno

from ansidocs.classes.abstract_project_part import AbstractProjectPart
from ansidocs.classes.abstract_project_part import AbstractDirContent
from ansidocs.classes.layout import Layout


logger = logging.getLogger(__name__)


@dataclass
class RolesDirContent(AbstractDirContent):
    """Class for keeping track of stuff in a plugin directory."""
    pass


class Roles(AbstractProjectPart):
    def __init__(self, project_root: str, layout: Layout):
        super().__init__(project_root=project_root, layout=layout)
        self.root_dir = path.abspath(path.join(self.project_root, layout.part_paths['roles']))
        if not path.exists(self.root_dir):
            raise FileNotFoundError(
                errno.ENOENT,
                f"Unable to find defaults project part directory {self.root_dir}",
                self.root_dir)


    def get_content(self):
        content = []
        subfiles = glob.glob(f'{self.root_dir}/*')
        content = filter(lambda f: path.isdir(f), subfiles)
        ret = RolesDirContent(subdirs=content)
        ret.parse_as_project = True
        return ret

    def to_markdown(self):
        relative_path = self.layout.part_paths['roles']
        markdown = ["### Roles", ""]
        content = self.get_content()

        if content.subdirs:
            markdown += ["The following roles are available for use:", ""]
            for role in content.subdirs:
                role_name = path.basename(role)
                markdown += [f"- [{role_name}]({path.join(relative_path, role_name)})"]
        else:
            markdown += ["There are no roles availble for this project."]
        return markdown
