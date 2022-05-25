import logging
import yaml
import textwrap
import os
from ..abstract_ansible_object import AnsibleObject
from src.classes.ansible_object_exceptions import AnsibleMetadataError
from src.classes.ansible_object_exceptions import MissingVariableDescription



logger = logging.getLogger(__name__)


class Role(AnsibleObject):

    def __init__(self, root_dir: str, namespace: str = None):
        self.root_dir = root_dir
        self.namespace = namespace
        self.type = 'role'

        self.__load_meta_attributes()

        try:
            logger.info(f"Role initiated with name {self.name} from directory {self.root_dir}")
        except AttributeError as e:
            raise AnsibleMetadataError(root_dir=root_dir, attribute_error=e)

    @property
    def name(self):
        return self.role_name

    @name.setter
    def name(self, name):
        self.role_name = name

    @property
    def qualified_name(self):
        return '.'.join([self.namespace, self.role_name])

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
        logger.debug("Reading in usage markdown file")
        try:
            with open(os.path.join(self.root_dir, 'docs/usage.md')) as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Unable to find a docs/usage.md. Using pre-formatted block as fallback")
            out = f"""
                This role can be included like any other role:
                ```
                - name: Example
                  hosts: localhost
                  roles:
                    - {self.name}
                ```
            """
        return textwrap.dedent(out)

    @property
    def variables(self):
        desc_dict = {}
        logger.debug("Loading variable defaults and descriptions")

        values_dict = self.__read_variable_default_values()
        desc_dict = self.__read_variable_descriptions()

        missing_descriptions = set(values_dict.keys()) - set(desc_dict.keys())
        if missing_descriptions:
            raise MissingVariableDescription(missing_variables=missing_descriptions)

        results_dict = {}
        for var_name in desc_dict:
            results_dict[var_name] = {}
            results_dict[var_name]['description'] = desc_dict[var_name]
            try:
                results_dict[var_name]['value'] = values_dict[var_name]
                results_dict[var_name]['required'] = False
            except KeyError:
                results_dict[var_name]['value'] = None
                results_dict[var_name]['required'] = True

        logger.debug("defaults dict: {0}".format(results_dict))
        return results_dict

    def __load_meta_attributes(self):
        logger.info("Loading data from meta/main.yml")
        try:
            with open(os.path.join(self.root_dir, 'meta/main.yml')) as file:
                meta_dict = yaml.safe_load(file)
                for k, v in meta_dict['galaxy_info'].items():
                    setattr(self, k, v)
        except FileNotFoundError as e:
            logger.exception("Exception parsing meta file: " + e)
            pass
        except KeyError:
            logger.exception("Unable to find galaxy_info object in meta. " +
                              "Is the file properly formatted?")

    def __read_variable_default_values(self):
        values_dict = {}
        try:
            with open(os.path.join(self.root_dir, 'defaults/main.yml')) as file:
                values_dict = yaml.safe_load(file) or {}
        except FileNotFoundError as e:
            logger.warning(e)

        return values_dict

    def __read_variable_descriptions(self):
        desc_dict = {}
        try:
            with open(os.path.join(self.root_dir, 'docs/defaults.yml')) as file:
                desc_dict = yaml.safe_load(file) or {}
        except FileNotFoundError as e:
            logger.warning(e)
            try:
                with open(os.path.join(self.root_dir, 'defaults/docs.md')) as file:
                    desc_dict = file.read()
            except FileNotFoundError:
                logger.warning(e)
        return desc_dict
