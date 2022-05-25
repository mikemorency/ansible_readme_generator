from setuptools import setup
from setuptools import find_packages

setup(
    name="ansidocs-mikemorency",
    version="0.0.1",
    packages=find_packages(),
    entry_points = {
        "console_scripts": [
            "ansidocs = src.command_line:main"
        ]
    },

    author="Mike Morency",
    author_email="mikemorency93@gmail.com",
    description="A command line tool to generate and update Ansible project READMEs",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/mikemorency/ansidocs",
    project_urls={
        "Bug Tracker": "https://github.com/mikemorency/ansidocs/issues",
    },
    install_requires=[
        'jinja2', 'pyyaml'
    ],
    optional_dependencies={
        "dev": ["ansible", "pytest"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
