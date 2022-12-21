from os import path
from os import listdir
import logging
from dataclasses import dataclass
import errno

from ansidocs.classes.abstract_project_part import AbstractProjectPart
from ansidocs.classes.abstract_project_part import AbstractDirContent
from ansidocs.classes.layout import Layout


logger = logging.getLogger(__name__)


@dataclass
class PlaybookDirContent(AbstractDirContent):
    """Class for keeping track of stuff in a playbooks directory."""
    playbooks: list
    subdirs: dict


class Playbooks(AbstractProjectPart):
    def __init__(self, project_root: str, layout: Layout):
        super().__init__(layout=layout, project_root=project_root)
        self.root_dir = path.abspath(path.join(self.project_root, layout.part_paths['playbooks']))
        if not path.exists(self.root_dir):
            raise FileNotFoundError(
                errno.ENOENT,
                f"Unable to find defaults project part directory {self.root_dir}",
                self.root_dir)


    def get_content(self, search_path: str = None):
        playbooks = []
        subdirs = {}
        ignore_dirs = ["templates", "files", "inventories", "group_vars"]
        if not search_path:
            search_path = self.root_dir

        for fsobj in listdir(search_path):
            obj_path = path.join(search_path, fsobj)
            if path.isdir(obj_path):
                if fsobj in ignore_dirs:
                    continue
                else:
                    nested_struct = self.get_content(obj_path)
                    subdirs[fsobj] = nested_struct
            else:
                if fsobj.endswith(".yml") or fsobj.endswith(".yaml"):
                    playbooks += [fsobj]
        return PlaybookDirContent(playbooks=playbooks, subdirs=subdirs)

    def to_markdown(self):
        relative_path = self.layout.part_paths['playbooks']
        markdown = ["### Playbooks", ""]
        content = self.get_content()

        for subdir_name, subdir_content in content.subdirs.items():
            markdown += self.__subdir_to_markdown(subdir_name, subdir_content)

        if content.playbooks:
            markdown += ["#### Other Plays", ""]
            for playbook in content.playbooks:
                markdown += [f"- [{playbook}]({path.join(relative_path, playbook)})"]
            markdown += [""]

        if len(markdown) == 2:   # header only
            markdown += ["There are no playbooks in the project."]
        else:
            markdown.insert(2, "The following playbooks are available to use from this project:")
            markdown.insert(3, "")
        return markdown

    def __subdir_to_markdown(self, subdir_name: str, subdir: PlaybookDirContent):
        relative_path = self.layout.part_paths['playbooks']
        markdown = [f"#### {str(subdir_name).capitalize()}", ""]
        if subdir.playbooks:
            for playbook in subdir.playbooks:
                markdown += [f"- [{playbook}]({path.join(relative_path, subdir_name, playbook)})"]
            markdown += [""]
        for child_name, child_subdir in subdir.subdirs.items():
            markdown += self.__subdir_to_markdown(f"{subdir_name}/{child_name}", child_subdir)

        if len(markdown) == 2:   # header only
            return []
        else:
            return markdown
