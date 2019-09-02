from setuptools import setup, find_packages

setup(
    # Application name:
    name="ictf_pipeline",

    # Version number (initial):
    version="1.1.5",

    # Application author details:
    author="Robert Longo",

    # Packages
    packages=find_packages(),

    # Include additional files into the package
    include_package_data=True,

    license="LICENSE",
    description="A project to generate paperwork required for ictf gradings.",

    long_description=open("README.md").read(),

    # Dependent packages (distributions)
    install_requires=[
        "fpdf",
        "pandas",
        "Pillow",
        "xlrd",
        "XlsxWriter"
    ],
)
