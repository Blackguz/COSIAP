import os
import sys

sys.path.insert(0, os.path.abspath('..'))  # Ensure the parent directory is included in sys.path

project = 'COSIAP'
copyright = '2023, Román Guzmán Valles'
author = 'Román Guzmán Valles'
release = '1.0.0'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []

language = 'ES'

html_theme = 'alabaster'
html_static_path = ['_static']
