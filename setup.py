from setuptools import find_packages, setup

dependencies = ["Click", "labelbox[data]"]

setup(
    name="labelbox-cli",
    version="0.0.1",
    description="CLI tool for managing Labelbox resources",
    author="Mihhail Matišinets",
    author_email="mihhail.matisinets@gmail.com",
    packages=find_packages(),
    install_requires=dependencies,
    entry_points={
        "console_scripts": [
            "labelbox = src.main:cli",
        ]
    },
)
