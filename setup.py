import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# get text of README.md
current_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(current_path, "README.md")) as f:
    readme_text = f.read()

setup(
    name = "gmailnator",
    version = '0.1.0',
    description = "Python wrapper for Gmailnator",
    long_description = readme_text,
    long_description_content_type = "text/markdown",
    url = "https://github.com/h0nde/py-gmailnator",
    author = "h0nde",
    email = "",
    license = "",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Email",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent"
    ],
    python_requires = '>=3',
    install_requires = [
        'requests'
    ],
    py_modules = ['gmailnator'],
    include_package_data = False
)
