import os
import yaml
import logging

from ansidocs.classes.layout import Layout


logger = logging.getLogger(__name__)


class Config():
    __raw_conf = {}
    __layouts = []

    def __init__(self, config_dir: str = None):
        if config_dir:
            self.load_file(config_dir)

    def load_file(self, config_dir: str = ""):
        config_path = os.getenv(
            "ANSIDOCS_CONFIG",
            os.path.abspath(os.path.join(config_dir, "ansidocs.yml"))
        )
        with open(config_path) as f:
            Config.__raw_conf = yaml.safe_load(f)
        self.__load_layouts()

    def __load_layouts(self):
        project_layouts = []
        for k, v in Config.__raw_conf.get('project_layouts', {}).items():
            project_layouts += [Layout(name=k, **v)]

        Config.__layouts = project_layouts

    @staticmethod
    def raw_config(name: str, default: None):
        return Config.__raw_conf.get(name, default)

    @staticmethod
    def layouts():
        logger.debug(Config.__layouts)
        return Config.__layouts
