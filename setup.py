from setuptools import setup
from setuptools import find_packages

setup(
    name="ansible_readme_generator",
    version="0.0.1",
    packages=find_packages(),
    entry_points = {
        "console_scripts": [
            "ansidocs = src.command_line:main"
        ]
    },

    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    install_requires=[
        'jinja2', 'pyyaml'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
