from ..abstract_ansible_object import AnsibleObject
import logging
import os
import yaml


logger = logging.getLogger(__name__)


class Collection(AnsibleObject):

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.type = 'collection'

        self.__load_meta_attributes()

        logger.info(f"Instantiated collection {self.qualified_name}")

    @property
    def qualified_name(self):
        return '.'.join([self.namespace, self.name])

    @property
    def roles(self):
        logger.debug("Loading roles from collection")
        roles_dir = os.path.join(self.root_dir, 'roles')
        roles = [
            d for d in os.listdir(roles_dir)
            if os.path.isdir(os.path.join(roles_dir, d))
        ]
        return roles

    @property
    def playbooks(self):
        return {
            "deployments": self.get_playbooks(subpath='deploy'),
            "configure": self.get_playbooks(subpath='configure'),
            "other": self.get_playbooks()
        }

    @property
    def plugins(self):
        logger.debug("Loading plugins from collection")
        plugin_dict = {}
        plugin_dir = os.path.join(self.root_dir, 'plugins')
        plugins = [d for d in os.listdir(plugin_dir)
                   if os.path.isdir(os.path.join(plugin_dir, d))]
        for plugin in plugins:
            for file in os.listdir(os.path.join(plugin_dir, plugin)):
                if file.endswith(".py") or file.endswith(".ps1"):
                    try:
                        plugin_dict[plugin] += [file]
                    except KeyError:
                        plugin_dict[plugin] = [file]
        return plugin_dict

    @property
    def description(self):
        logger.debug("Reading in description markdown file")
        try:
            with open(os.path.join(self.root_dir, 'docs/description.md')) as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Unable to find a docs/description.md. Using meta description as fallback")
            return self._meta_description

    @description.setter
    def description(self, description):
        self._meta_description = description

    @property
    def usage(self):
        try:
            with open(os.path.join(self.root_dir, 'docs/usage.md')) as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Unable to find a docs/usage.md. Will use template")
            return None

    def __load_meta_attributes(self):
        logger.info("Loading data from galaxy.yml")
        try:
            with open(os.path.join(self.root_dir, 'galaxy.yml')) as file:
                meta_dict = yaml.safe_load(file)
                for k, v in meta_dict.items():
                    setattr(self, k, v)
        except FileNotFoundError as e:
            logger.exception(f"Exception parsing galaxy file: {e}")
            pass

    def get_playbooks(self, subpath: str = ''):
        logger.debug(f"Loading playbooks from collection playbook/{subpath}")
        play_list = []
        play_dir = os.path.join(self.root_dir, 'playbooks', subpath)
        if os.path.isdir(play_dir):
            for file in os.listdir(play_dir):
                if file.endswith(".yml") or file.endswith(".yaml"):
                    play_list += [os.path.join('playbooks', subpath, file)]

        return play_list
