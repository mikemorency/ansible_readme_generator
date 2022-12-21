from dataclasses import dataclass
from dataclasses import field


@dataclass
class MetaLayout:
    file: str
    name_attr: str = field(default_factory=lambda: "name")
    nested_key: str = field(default_factory=lambda: None)


@dataclass
class Layout:
    """Class for describing a project type layout."""
    name: str
    meta: MetaLayout
    readme: str = field(default_factory=lambda: "./README.md")
    docs: str = field(default_factory=lambda: "./docs")
    part_paths: dict = field(default_factory=lambda: {})
    part_namespace: str = field(default_factory=lambda: None)

    def __post_init__(self):
        self.meta = MetaLayout(
            file=self.meta['file'],
            name_attr=self.meta.get('name_attr', 'name'),
            nested_key=self.meta.get('nested_key', '')
        )
        self.part_paths = dict(sorted(self.part_paths.items()))
