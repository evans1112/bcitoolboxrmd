
project = 'BCI Toolbox'
author = 'Evans'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',  # 自动生成API文档
    'sphinx.ext.viewcode',  # 添加源码链接
]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_material"  # 将主题改为 sphinx_material

# 在下面添加更多的主题选项，根据需要自定义配置
html_theme_options = {
    'color_primary': 'blue',
    'color_accent': 'light-blue',
    'logo_icon': '&#xe869',
    'logo_text': 'BCI Toolbox',
    'globaltoc_depth': 3,
}
