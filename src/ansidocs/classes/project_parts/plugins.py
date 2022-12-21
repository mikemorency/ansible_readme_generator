from os import path
from os import listdir
from dataclasses import dataclass
import errno

from ansidocs.classes.abstract_project_part import AbstractProjectPart
from ansidocs.classes.abstract_project_part import AbstractDirContent
from ansidocs.classes.layout import Layout


@dataclass
class PluginDirContent(AbstractDirContent):
    """Class for keeping track of stuff in a plugin directory."""
    plugins: list
    subdirs: dict


class Plugins(AbstractProjectPart):
    def __init__(self, project_root: str, layout: Layout):
        super().__init__(layout=layout, project_root=project_root)
        self.root_dir = path.abspath(path.join(self.project_root, layout.part_paths['plugins']))
        if not path.exists(self.root_dir):
            raise FileNotFoundError(
                errno.ENOENT,
                f"Unable to find defaults project part directory {self.root_dir}",
                self.root_dir)


    def get_content(self, search_path: str = None):
        plugins = []
        subdirs = {}
        if not search_path:
            search_path = self.root_dir

        for fsobj in listdir(search_path):
            obj_path = path.join(search_path, fsobj)
            if path.isdir(obj_path):
                nested_struct = self.get_content(obj_path)
                subdirs[fsobj] = nested_struct
            else:
                if fsobj.endswith(".py") or fsobj.endswith(".ps1"):
                    plugins += [fsobj]
        return PluginDirContent(plugins=plugins, subdirs=subdirs)

    def to_markdown(self):
        relative_path = self.layout.part_paths['plugins']
        markdown = ["### Plugins", ""]
        content = self.get_content()

        for subdir_name, subdir_content in content.subdirs.items():
            markdown += self.__subdir_to_markdown(subdir_name, subdir_content)

        if content.plugins:
            markdown += ["#### Other Plugins", ""]
            for plugin in content.plugins:
                markdown += [f"- [{plugin}]({path.join(relative_path, plugin)})"]
            markdown += [""]

        if len(markdown) == 2:   # header only
            markdown += ["There are no plugins in this project."]
        else:
            markdown.insert(2, "The following plugins are available to use from this project:")
            markdown.insert(3, "")
        return markdown

    def __subdir_to_markdown(self, subdir_name: str, subdir: PluginDirContent):
        markdown = [f"#### {str(subdir_name).capitalize()}", ""]
        if subdir.plugins:
            for plugin in subdir.plugins:
                markdown += [f"- [{plugin}]({path.join(subdir_name, plugin)})"]
            markdown += [""]
        for child_name, child_subdir in subdir.subdirs.items():
            markdown += self.__subdir_to_markdown(f"{subdir_name}/{child_name}", child_subdir)

        if len(markdown) == 2:   # header only
            return []
        else:
            return markdown
