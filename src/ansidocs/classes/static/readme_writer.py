import logging
from os import path
import jinja2

from ansidocs.classes.project import Project


logger = logging.getLogger(__name__)


class ReadmeWriter():
    __jinja_env = {}

    def __init__(self, config_dir: str = None):
        if config_dir:
            self.load_templates(config_dir)

    def load_templates(self, config_dir: str):
        loader = jinja2.FileSystemLoader(path.join(config_dir, 'templates'), encoding='utf8')
        ReadmeWriter.__jinja_env = jinja2.Environment(loader=loader, autoescape=True)
        ReadmeWriter.__jinja_env.filters['basename'] = basename

    @staticmethod
    def jinja_env():
        return ReadmeWriter.__jinja_env

    @staticmethod
    def update(project: Project):
        logger.info(f"Updating readme for project, {project.readme_file}")
        try:
            readme_template = ReadmeWriter.__jinja_env.get_template(f'{project.layout.name}/README.md.j2')
        except jinja2.exceptions.TemplateNotFound:
            logger.debug(f"No custom readme template for layout '{project.layout.name}'")
            readme_template = ReadmeWriter.__jinja_env.get_template('defaults/README.md.j2')

        description_block = ReadmeWriter.__render_description(project=project)
        usage_block = ReadmeWriter.__render_usage(project=project)
        footer_block = ReadmeWriter.__render_footer(project=project)

        readme_text = readme_template.render(
            description_block=description_block,
            usage_block=usage_block,
            footer_block=footer_block
        )
        logger.info("Writing data to readme")
        with open(path.join(project.root_dir, project.readme_file), 'w') as file:
            file.write(readme_text)

    @staticmethod
    def __render_description(project: Project):
        logger.info("Compiling description section of readme for project")
        try:
            template = ReadmeWriter.__jinja_env.get_template(f'{project.layout.name}/description.md.j2')
        except jinja2.exceptions.TemplateNotFound:
            logger.debug(f"No custom description readme template for layout '{project.layout.name}'")
            template = ReadmeWriter.__jinja_env.get_template('defaults/description.md.j2')
        return template.render(project=project)

    @staticmethod
    def __render_usage(project: Project):
        logger.info("Compiling usage section of readme for project")
        try:
            template = ReadmeWriter.__jinja_env.get_template(f'{project.layout.name}/usage.md.j2')
        except jinja2.exceptions.TemplateNotFound:
            logger.debug(f"No custom usage readme template for layout '{project.layout.name}'")
            template = ReadmeWriter.__jinja_env.get_template('defaults/usage.md.j2')
        return template.render(project=project)

    @staticmethod
    def __render_footer(project: Project):
        logger.info("Compiling footer section of readme for project")
        try:
            template = ReadmeWriter.__jinja_env.get_template(f'{project.layout.name}/footer.md.j2')
        except jinja2.exceptions.TemplateNotFound:
            logger.debug(f"No custom footer readme template for layout '{project.layout.name}'")
            template = ReadmeWriter.__jinja_env.get_template('defaults/footer.md.j2')
        return template.render(project=project)


def basename(path):
    return path.basename(path)
