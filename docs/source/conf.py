import os
import sys

os.environ["SPHINX_BUILD"] = "1"
sys.path.insert(0, os.path.abspath('../..'))  # Explicit path to the project root

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'FPL Dashboard'
copyright = '2025, Othmane Mahfoud'
author = 'Othmane Mahfoud'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # Automatically document docstrings
    "sphinx.ext.napoleon",  # Support for Google-style and NumPy-style docstrings
]

exclude_patterns = [
    "tests/*",  # Exclude the tests folder
    "app.py",   # Exclude app.py
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
