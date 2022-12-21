from abc import ABC
from abc import abstractmethod
from typing import Iterable
from dataclasses import dataclass
from dataclasses import field
from os import path

from ansidocs.classes.layout import Layout


@dataclass
class AbstractDirContent(ABC):
    subdirs: Iterable
    parse_as_project: bool = field(default=False, init=False)


class AbstractProjectPart(ABC):
    def __init__(self, project_root: str, layout: Layout):
        self.project_root = path.abspath(project_root)
        self.layout = layout

    @abstractmethod
    def get_content():
        pass

    @abstractmethod
    def to_markdown() -> Iterable:
        pass

    def link_project(self, project: object):
        self.project = project
