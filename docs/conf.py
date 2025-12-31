# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'flagos-docs-portal'
copyright = '2025, FlagOS Community'
author = 'FlagOS Community'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

source_suffix = '.md'

exclude_patterns = [
    'README.md',      # 排除所有子目录中的 README.md
    'README-en.md',   # 排除所有子目录中的 README.en.md
]

extensions = [
    "myst_parser",
    # "autodoc2",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_design",
    "sphinx_copybutton",
    # "sphinxext.rediraffe",
    # disabled due to https://github.com/mgaitan/sphinxcontrib-mermaid/issues/109
    "sphinxcontrib.mermaid",
    "sphinxext.opengraph",
    "sphinx_pyscript",
    # "sphinx_tippy",
    "sphinx_togglebutton",
]

templates_path = ['_templates']
exclude_patterns = []


myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "deflist",
    "fieldlist",
    "html_admonition",
    "html_image",
    "colon_fence",
    "smartquotes",
    "replacements",
    # "linkify",
    "strikethrough",
    "substitution",
    "tasklist",
    "attrs_inline",
    "attrs_block",
]
myst_url_schemes = {
    "http": None,
    "https": None,
    "mailto": None,
    "ftp": None,
    "wiki": "https://en.wikipedia.org/wiki/{{path}}#{{fragment}}",
    "doi": "https://doi.org/{{path}}",
    "gh-pr": {
        "url": "https://github.com/executablebooks/MyST-Parser/pull/{{path}}#{{fragment}}",
        "title": "PR #{{path}}",
        "classes": ["github"],
    },
    "gh-issue": {
        "url": "https://github.com/executablebooks/MyST-Parser/issue/{{path}}#{{fragment}}",
        "title": "Issue #{{path}}",
        "classes": ["github"],
    },
    "gh-user": {
        "url": "https://github.com/{{path}}",
        "title": "@{{path}}",
        "classes": ["github"],
    },
}
myst_number_code_blocks = ["typescript"]
myst_heading_anchors = 2
myst_footnote_transition = True
myst_dmath_double_inline = True
myst_enable_checkboxes = True
myst_substitutions = {
    "role": "[role](#syntax/roles)",
    "directive": "[directive](#syntax/directives)",
}



# -- Options for sphinx-intl example

locale_dirs = ['locale/']   # po files will be created in this directory
gettext_compact = False     # optional: avoid file concatenation in sub directories.

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
# html_static_path = ['_static']

html_theme = "sphinx_book_theme"
html_logo = "_static/logo.png"
html_favicon = "_static/logo.png"
html_title = ""
html_theme_options = {
    "logo": {
      "image_light": "_static/logo.png",
      "image_dark": "_static/logo.png",
   },
    "home_page_in_toc": True,
    "use_download_button": False,
    "repository_url": "https://github.com/flagos-ai/KernelGen",
    "use_edit_page_button": True,
    # "github_url": "https://github.com/flagos-ai/KernelGen",
    # "repository_branch": "master",
    # "path_to_docs": "docs",
    "use_repository_button": True,
    # "announcement": "<b>v3.0.0</b> is now out! See the Changelog for details",
}
html_last_updated_fmt = ""
# OpenGraph metadata
ogp_site_url = "https://myst-parser.readthedocs.io/en/latest"
# This is the image that GitHub stores for our social media previews
ogp_image = "https://repository-images.githubusercontent.com/240151150/316bc480-cc23-11eb-96fc-4ab2f981a65d"
ogp_custom_meta_tags = [
    '<meta name="twitter:card" content="summary_large_image">',
]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["local.css"]

rediraffe_redirects = {
    "using/intro.md": "sphinx/intro.md",
    "syntax/syntax.md": "syntax/typography.md",
    "sphinx/intro.md": "intro.md",
    "using/use_api.md": "api/index.md",
    "api/index.md": "api/reference.rst",
    "api/reference.rst": "apidocs/index.md",
    "using/syntax.md": "syntax/syntax.md",
    "using/syntax-optional.md": "syntax/optional.md",
    "using/reference.md": "syntax/reference.md",
    "sphinx/reference.md": "configuration.md",
    "sphinx/index.md": "faq/index.md",
    "sphinx/use.md": "faq/index.md",
    "sphinx/faq.md": "faq/index.md",
    "explain/index.md": "develop/background.md",
}

# tippy_skip_anchor_classes = ("headerlink", "sd-stretched-link", "sd-rounded-pill")
# tippy_anchor_parent_selector = "article.bd-article"
# tippy_rtd_urls = [
#     "https://www.sphinx-doc.org/en/master",
#     "https://markdown-it-py.readthedocs.io/en/latest",
# ]
# # TODO failing
# tippy_enable_wikitips = False
