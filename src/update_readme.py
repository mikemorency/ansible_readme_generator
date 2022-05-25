import logging
import os
from src.classes.ansible_object_factory import AnsibleObjectFactory
from src.classes.abstract_ansible_object import AnsibleObject
from datetime import datetime
import jinja2


logger = logging.getLogger(__name__)


def update_readme(ansible_object: AnsibleObject, readme_file: str = 'README.md'):
    logger.info(f"Creating object for {ansible_object.type} {ansible_object.qualified_name}")
    loader = jinja2.FileSystemLoader(os.path.join(
                    os.path.dirname(__file__), 'templates'), encoding='utf8')
    env = jinja2.Environment(loader=loader, autoescape=True)
    template = env.get_template('README.md.j2')

    env.filters['basename'] = basename

    readme_text = template.render(
        ansi_obj=ansible_object,
        updater=os.path.basename(__file__),
        time=datetime.now())

    logger.info("Writing data to readme")
    with open(os.path.join(ansible_object.root_dir, readme_file), 'w') as file:
        file.write(readme_text)

    if ansible_object.type == 'collection':
        for role in ansible_object.roles:
            logger.info("Updating readme for collection's role : {0}".format(role))
            update_readme(
                ansible_object=AnsibleObjectFactory().create_object(
                    os.path.join(ansible_object.root_dir, 'roles', role),
                    namespace=ansible_object.qualified_name))


def basename(path):
    return os.path.basename(path)


def main(directory: str, loglevel: str):
    logger.basicConfig(level=loglevel)
    directory = directory.rstrip('/')
    logger.debug(f"Directory : {directory}")

    ansible_object = AnsibleObjectFactory().create_object(directory)
    update_readme(ansible_object)
