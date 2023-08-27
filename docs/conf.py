import sphinx_readable_theme
project = 'BCI Toolbox'
author = 'Evans'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',  # 自动生成API文档
    'sphinx.ext.viewcode',  # 添加源码链接
]

# -- Options for HTML output -------------------------------------------------

html_theme = 'readable'
html_theme_path = [sphinx_readable_theme.get_html_theme_path()]
