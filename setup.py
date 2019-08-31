from setuptools import setup, find_packages

setup(
    # Application name:
    name="ictf_pipeline",

    # Version number (initial):
    version="1.1.3",

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
        "astroid==2.2.5",
        "fpdf==1.7.2",
        "isort==4.3.17",
        "lazy-object-proxy==1.3.1",
        "mccabe==0.6.1",
        "numpy==1.16.2",
        "pandas==0.24.2",
        "Pillow==6.0.0",
        "pylint==2.3.1",
        "python-dateutil==2.8.0",
        "pytz==2019.1",
        "six==1.12.0",
        "typed-ast==1.3.4",
        "wrapt==1.11.1",
        "xlrd==1.2.0",
        "XlsxWriter==1.1.6"
    ],
)
