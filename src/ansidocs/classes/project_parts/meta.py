import logging
from os import path
import yaml
import errno

from ansidocs.classes.layout import MetaLayout


logger = logging.getLogger(__name__)


class Meta:
    def __init__(self, layout: MetaLayout, project_root: str, namespace: str = None):
        super().__init__()
        self.description = ""
        self.layout = layout
        self.name = path.basename(project_root)
        meta_abs = path.abspath(path.join(project_root, layout.file))
        if not path.exists(meta_abs):
            raise FileNotFoundError(
                errno.ENOENT,
                f"Unable to find meta file {meta_abs}",
                meta_abs)


        with open(meta_abs, "r") as f:
            meta_data = yaml.safe_load(f)

        if layout.nested_key:
            self.__dict__.update(meta_data[layout.nested_key])
        else:
            self.__dict__.update(meta_data)

        try:
            self.name = self.__dict__[layout.name_attr]
        except KeyError:
            pass


        if namespace:
            self.namespace = namespace

        try:
            self.qualified_name = ".".join([self.namespace, self.name])
        except AttributeError as e:
            logger.debug(f"Missing piece of qualified name from meta file, {e}")
            self.qualified_name = None
