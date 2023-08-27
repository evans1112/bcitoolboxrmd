project = 'BCI Toolbox'
author = 'Evans'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',  # 自动生成API文档
    'sphinx.ext.viewcode',  # 添加源码链接
]

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_material'  # 使用的主题，可以选择其他主题
html_static_path = ['_static']
