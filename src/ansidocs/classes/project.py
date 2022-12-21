import logging
from os import path

from ansidocs.classes.layout import Layout
from ansidocs.classes.project_parts.meta import Meta
from ansidocs.classes.project_parts.playbooks import Playbooks   # noqa: F401
from ansidocs.classes.project_parts.plugins import Plugins   # noqa: F401
from ansidocs.classes.project_parts.defaults import Defaults   # noqa: F401
from ansidocs.classes.project_parts.roles import Roles   # noqa: F401


logger = logging.getLogger(__name__)


class Project():
    def __init__(self, layout: Layout, root_dir: str, namespace: str = None):
        self.root_dir = path.abspath(root_dir)
        if not path.exists(self.root_dir):
            raise FileNotFoundError(f"Unable to find project directory {self.root_dir}")

        abs_doc_dir = path.abspath(path.join(self.root_dir, layout.docs))
        if not path.exists(abs_doc_dir):
            logger.warning(f"Unable to find documentation directory in project, {abs_doc_dir}")
            self.docs_dir = None
        else:
            self.docs_dir = abs_doc_dir

        self.meta = Meta(layout=layout.meta, project_root=self.root_dir, namespace=namespace)
        self.layout = layout
        self.parts = self.__find_parts(layout.part_paths)
        self.readme_file = path.join(self.root_dir, layout.readme)
        self._description = None
        self._usage = None

    def __find_parts(self, part_paths: dict):
        results = []
        for k, v in part_paths.items():
            logger.debug(f"Looking for part {k=} and path {v=}")
            try:
                part_class = globals()[str(k).capitalize()]
                results += [part_class(project_root=self.root_dir, layout=self.layout)]
                logger.info(f"Loaded project part {k}")
            except KeyError:
                raise Exception(f"This program does not support project part '{k}'"
                                f" from the layout configuration '{self.layout.name}'")
            except FileNotFoundError as e:
                logger.warning(f"Could not find project part {k} at {e.filename}")

        return set(results)

    @property
    def description(self):
        if self._description:
            return self._description

        self._description = self.meta.description
        if self.docs_dir:
            logger.debug("Looking for a custom description.md file for this project")
            try:
                with open(path.join(self.docs_dir, "description.md")) as f:
                    self._description = f.read()
            except FileNotFoundError:
                logger.debug("Unable to find a description.md in docs directory. Using meta description as fallback")
        else:
            logger.debug("No docs directory. Using meta description as fallback")

        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def usage(self):
        if self._usage:
            return self._usage

        self._usage = None
        if self.docs_dir:
            logger.debug("Looking for a custom usage.md file for this project")
            try:
                with open(path.join(self.docs_dir, "usage.md")) as f:
                    self._usage = f.read()
            except FileNotFoundError:
                logger.info("Unable to find a custom usage.md in docs directory")
        else:
            logger.debug("No docs directory.No custom usage markdown will be added")

        return self._usage
