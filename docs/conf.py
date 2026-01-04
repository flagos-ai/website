"""
Shared Sphinx configuration using sphinx-multiproject.

To build each project, the ``PROJECT`` environment variable is used.

.. code:: console

   $ make html  # build default project
   $ PROJECT=flagos_en make html  # build the flagos English project
   $ PROJECT=flagcx_en make html  # build the flagcx English project
   $ PROJECT=flaggems_en make html  # build the flaggems English project
   $ PROJECT=flagtree_en make html  # build the flagtree English project
   $ PROJECT=flagrelease_en make html  # build the lagrelease English project
   $ PROJECT=flagperf_en make html  # build the flagperf English project
   $ PROJECT=zh make html  # build the Chinese project

For more information read https://sphinx-multiproject.readthedocs.io/.
"""

import os
import sys

# Fix imports: Check different import methods
try:
    # First try sphinx_multiproject
    from sphinx_multiproject.utils import get_project
    print("INFO: Using sphinx_multiproject")
except ImportError:
    try:
        # Then try multiproject
        from multiproject.utils import get_project
        print("INFO: Using multiproject")
    except ImportError:
        # If both fail, create a simple get_project function
        print("WARNING: sphinx-multiproject not found. Using simple project selection.")
        def get_project(projects):
            return os.environ.get("PROJECT", "flagos_en")

sys.path.append(os.path.abspath("_ext"))

# Base extensions - only include actually installed ones
extensions = [
    "multiproject",  # Sphinx extension name, not Python module name
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    # Temporarily comment out potentially problematic extensions
    # "sphinx_tabs.tabs",  # Module name might be different
    # "sphinx_prompt",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    # Comment out uninstalled extensions
    # "sphinxcontrib.httpdomain",
    # "sphinxcontrib.video",
    # "sphinxemoji.sphinxemoji",
    "sphinxext.opengraph",
]

# Check and add actually installed extensions
try:
    import sphinx_tabs
    extensions.append("sphinx_tabs.tabs")
    print("INFO: sphinx_tabs extension added")
except ImportError:
    print("INFO: sphinx_tabs not available")

try:
    import sphinx_prompt
    extensions.append("sphinx_prompt")
    print("INFO: sphinx_prompt extension added")
except ImportError:
    print("INFO: sphinx_prompt not available")

multiproject_projects = {
    "flagos_en": {
        "use_config_file": False,
        "config": {
            "project": "Documentation",
            "html_title": "FlagOS Documentation",
        },
    },
    "zh": {
        "use_config_file": False,
        "config": {
            "project": "FlagOS Documentation Center",
            "html_title": "FlagOS Documentation Center",
        },
    },
}

docset = get_project(multiproject_projects)

ogp_site_name = "KernelGen Documentation"
ogp_use_first_image = True
ogp_image = "https://docs.readthedocs.io/en/latest/_static/img/logo-opengraph.png"
ogp_custom_meta_tags = (
    '<meta name="twitter:card" content="summary_large_image" />',
)
ogp_enable_meta_description = True
ogp_description_length = 300

templates_path = ["_templates"]
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")

master_doc = "index"
copyright = '2025, FlagOS Community'
author = 'FlagOS Community'
release = '1.0.0'
# release = version
exclude_patterns = ["_build", "shared", "_includes"]
if docset == "zh":
    exclude_patterns.append("flagos_en")
elif docset == "flagos_en":
    exclude_patterns.append("zh")
default_role = "obj"
intersphinx_cache_limit = 14
intersphinx_timeout = 3
intersphinx_mapping = {
    "python": ("https://docs.python.org/3.10/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

intersphinx_disabled_reftypes = ["*"]

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
htmlhelp_basename = "KernelGendoc"
latex_documents = [
    (
        "index",
        "KernelGen.tex",
        "KernelGen Documentation",
        "KernelGen Team",
        "manual",
    ),
]
man_pages = [
    (
        "index",
        "kernelgen",
        "KernelGen Documentation",
        ["KernelGen Team"],
        1,
    )
]

# language = "en" if docset == "en" else "zh_CN"

language = "en" if docset.endswith("_en") else "zh_CN"

locale_dirs = [
    f"{docset}/locale/",
]
gettext_compact = False

html_short_title = ""

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static", f"{docset}/_static"]
html_css_files = ["custom.css", "homepage.css"]
# Do not add sphinx_prompt_css.css for now, it might not exist
html_js_files = []

html_logo = "img/logo.png"
html_favicon = "img/logo.png"
# html_theme_options = {
#     "logo_only": True,
# }

html_sidebars = {
    "zh/index": [],
    "flagos_en/index": [],
}

html_theme_options = {
    # "logo_only": False,
    "logo": {
        "text": "Documentation",
        # "image_light": "_static/logo-light.png",
        # "image_dark": "_static/logo-dark.png",
    },
    "home_page_in_toc": True,
    "use_download_button": False,
    "repository_url": "https://github.com/flagos-ai/KernelGen",
    # "use_edit_page_button": True,
    # "github_url": "https://github.com/flagos-ai/KernelGen",
    # "repository_branch": "master",
    # "path_to_docs": "docs",
    "use_repository_button": True,
    # "announcement": "<b>v3.0.0</b> is now out! See the Changelog for details",
    "secondary_sidebar_items": {
        "zh/index": [],
        "flagos_en/index": [],
    },
    "footer_start": ["copyright"],
    "footer_end": [],
    "show_sphinx": False,
    # Note we have omitted `theme-switcher` below
    "navbar_end": ["navbar-icon-links"]
}

html_context = {
    "default_mode": "dark"
# #     "conf_py_path": f"/docs/{docset}/",
#     # "display_github": True,
#     "github_user": "armstrongttwalker-alt",
#     "github_repo": "https://github.com/flagos-ai/KernelGen",
# #     "github_version": "main",
# #     "plausible_domain": f"{os.environ.get('READTHEDOCS_PROJECT')}.readthedocs.io",
}

rst_epilog = """
.. |org_brand| replace:: KernelGen Community
.. |com_brand| replace:: KernelGen for Business
.. |git_providers_and| replace:: GitHub, Bitbucket, and GitLab
.. |git_providers_or| replace:: GitHub, Bitbucket, or GitLab
"""

autosectionlabel_prefix_document = True

linkcheck_retries = 2
linkcheck_timeout = 1
linkcheck_workers = 10
linkcheck_ignore = [
    r"http://127\.0\.0\.1",
    r"http://localhost",
    r"https://github\.com.+?#L\d+",
]

extlinks = {
    "issue": ("https://github.com/armstrongttwalker-alt/test-i18n-KernelGen/issues/%s", "#%s"),
}

suppress_warnings = ["epub.unknown_project_files"]