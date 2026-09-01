
project = 'BCI Toolbox'
author = 'Evans'
version = '0.3'
release = '0.3.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'myst_parser',
]

# The v0.3.0 programmatic API is authored in Markdown in the Python package.
# MyST lets those source files remain the single source of truth while still
# participating in the Sphinx navigation and cross-page links.
myst_heading_anchors = 4

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
html_logo = '_static/BCI.png'
html_static_path = ['_static']
html_extra_path = ['examples']
html_css_files = ['custom-material-style.css']
html_theme_options = {
    'description': 'Bayesian Causal Inference Toolbox',
    'fixed_sidebar': True,
    'page_width': '1120px',
    'sidebar_width': '260px',
}
