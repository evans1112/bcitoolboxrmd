
project = 'BCI Toolbox'
author = 'Evans'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
html_logo = '_static/BCI.png'
html_static_path = ['_static']
html_css_files = ['custom-material-style.css']
html_theme_options = {
    'description': 'Bayesian Causal Inference Toolbox',
    'fixed_sidebar': True,
    'page_width': '1120px',
    'sidebar_width': '260px',
}
