import logging
import os
import shutil
import pathlib

from ansidocs.classes.project import Project
from ansidocs.classes.static.config import Config
from ansidocs.classes.static.readme_writer import ReadmeWriter
from ansidocs.classes.exceptions import UknownLayoutException


logger = logging.getLogger(__name__)


def determine_project_layout(project_path: str, force_layout: str = None):
    full_dir = os.path.abspath(project_path)
    if not os.path.exists(full_dir):
        raise FileNotFoundError(f"Unable to find any files at {project_path}")

    if force_layout:
        try:
            return Config.layouts()[force_layout]
        except KeyError:
            logger.critical(f"Unable to find user requested layout {force_layout} in config")
    else:
        for layout in Config.layouts():
            if os.path.exists(os.path.join(full_dir, layout.meta.file)):
                return layout
    return None


def process_directory(project_path: str, namespace: str = None, force_layout: str = None):
    layout = determine_project_layout(project_path=project_path, force_layout=force_layout)
    if not layout:
        raise UknownLayoutException(project_directory=project_path)

    project = Project(root_dir=project_path, layout=layout, namespace=namespace)
    if layout.part_namespace and layout.part_namespace != 'none':
        try:
            part_namespace = getattr(project.meta, layout.part_namespace)
        except AttributeError:
            logger.critical(f"Unrecognized attribute '{layout.part_namespace}' "
                            "on parent project. Cant set part namespace.")
            raise
    else:
        part_namespace = None

    for part in project.parts:
        content = part.get_content()
        if content.parse_as_project:
            for subdir in content.subdirs:
                process_directory(project_path=subdir, namespace=part_namespace)

    ReadmeWriter.update(project)


def init_config_dir(config_dir: str, refresh_configs: bool = False):
    if refresh_configs:
        logger.warning("Config refresh requested. Config directory will be removed and recreated")
        try:
            shutil.rmtree(config_dir)
        except FileNotFoundError:
            pass
    if not os.path.exists(config_dir):
        logger.info(f"No config directory exists, creating one at {config_dir} with defaults now")
        current_file_path = pathlib.Path(__file__).parent.resolve()
        shutil.copytree(f"{current_file_path}/config", config_dir)
        os.chmod(config_dir, 0o755)
        for root, dirs, files in os.walk(config_dir):
            for dir in dirs:
                os.chmod(os.path.join(root, dir), 0o755)
            for file in files:
                os.chmod(os.path.join(root, file), 0o644)
    else:
        logger.info(f"Config directory exists at {config_dir}")


def generate(directory: str, config_dir: str = "ansidocs/config", force_layout: str = None):
    directory = directory.rstrip('/')
    logger.debug(f"{directory=}")
    logger.debug(f"{config_dir=}")
    init_config_dir(config_dir=config_dir)

    Config().load_file(config_dir)
    ReadmeWriter().load_templates(config_dir)
    try:
        process_directory(project_path=directory, force_layout=force_layout)
    except Exception as e:
        logger.critical(e)
        logger.critical("Caught fatal exception and exiting. See output above")
    else:
        logger.info("Done, finished updating readmes successfully")


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    project_root = "/tmp/test"
    generate(directory=project_root)
