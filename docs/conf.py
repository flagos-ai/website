"""
Shared Sphinx configuration using sphinx-multiproject.

To build each project, the ``PROJECT`` environment variable is used.

.. code:: console

   $ make html  # build default project
   $ PROJECT=flagos_en make html  # build the flagos English project
   $ PROJECT=flagcx_en make html  # build the flagcx English project
   $ PROJECT=flaggems_en make html  # build the flaggems English project
   $ PROJECT=flagtree_en make html  # build the flagtree English project
   $ PROJECT=flagrelease_en make html  # build the flagrelease English project
   $ PROJECT=flagperf_en make html  # build the flagperf English project
   $ PROJECT=flagos_zh make html  # build the flagos Chinese project
   $ PROJECT=flagcx_zh make html  # build the flagcx Chinese project
   $ PROJECT=flaggems_zh make html  # build the flaggems Chinese project
   $ PROJECT=flagtree_zh make html  # build the flagtree Chinese project
   $ PROJECT=flagrelease_zh make html  # build the flagrelease Chinese project
   $ PROJECT=flagperf_zh make html  # build the flagperf Chinese project

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
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
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

# Define all projects
multiproject_projects = {
    # English projects
    "flagos_en": {
        "use_config_file": False,
        "config": {
            "project": "FlagOS Documentation",
            "html_title": "FlagOS Documentation",
        },
    },
    "flagcx_en": {
        "use_config_file": False,
        "config": {
            "project": "FlagCX Documentation",
            "html_title": "FlagCX Documentation",
        },
    },
    "flaggems_en": {
        "use_config_file": False,
        "config": {
            "project": "FlagGems Documentation",
            "html_title": "FlagGems Documentation",
        },
    },
    "flagtree_en": {
        "use_config_file": False,
        "config": {
            "project": "FlagTree Documentation",
            "html_title": "FlagTree Documentation",
        },
    },
    "flagrelease_en": {
        "use_config_file": False,
        "config": {
            "project": "FlagRelease Documentation",
            "html_title": "FlagRelease Documentation",
        },
    },
    "flagperf_en": {
        "use_config_file": False,
        "config": {
            "project": "FlagPerf Documentation",
            "html_title": "FlagPerf Documentation",
        },
    },
    # Chinese projects
    "flagos_zh": {
        "use_config_file": False,
        "config": {
            "project": "FlagOS 文档中心",
            "html_title": "FlagOS 文档中心",
        },
    },
    "flagcx_zh": {
        "use_config_file": False,
        "config": {
            "project": "FlagCX 文档中心",
            "html_title": "FlagCX 文档中心",
        },
    },
    "flaggems_zh": {
        "use_config_file": False,
        "config": {
            "project": "FlagGems 文档中心",
            "html_title": "FlagGems 文档中心",
        },
    },
    "flagtree_zh": {
        "use_config_file": False,
        "config": {
            "project": "FlagTree 文档中心",
            "html_title": "FlagTree 文档中心",
        },
    },
    "flagrelease_zh": {
        "use_config_file": False,
        "config": {
            "project": "FlagRelease 文档中心",
            "html_title": "FlagRelease 文档中心",
        },
    },
    "flagperf_zh": {
        "use_config_file": False,
        "config": {
            "project": "FlagPerf 文档中心",
            "html_title": "FlagPerf 文档中心",
        },
    },
}

# Get current project
docset = get_project(multiproject_projects)

# OGP configuration
ogp_site_name = "KernelGen Documentation"
ogp_use_first_image = True
ogp_image = "https://docs.readthedocs.io/en/latest/_static/img/logo-opengraph.png"
ogp_custom_meta_tags = (
    '<meta name="twitter:card" content="summary_large_image" />',
)
ogp_enable_meta_description = True
ogp_description_length = 300

# Path configuration
templates_path = ["_templates"]
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")

# Basic information
master_doc = "index"
copyright = '2025, FlagOS Community'
author = 'FlagOS Community'
release = '1.0.0'

# Exclude patterns - exclude all other project directories
exclude_patterns = ["_build", "shared", "_includes"]

# Get all project directories to exclude
all_projects = list(multiproject_projects.keys())
for project in all_projects:
    if project != docset:
        # Exclude both the project directory and any subdirectories
        exclude_patterns.append(f"{project}/*")
        exclude_patterns.append(f"{project}/**/*")

default_role = "obj"

# Intersphinx configuration
intersphinx_cache_limit = 14
intersphinx_timeout = 3
intersphinx_mapping = {
    "python": ("https://docs.python.org/3.10/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_reftypes = ["*"]

# MyST extensions
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
    "strikethrough",
    "substitution",
    "tasklist",
    "attrs_inline",
    "attrs_block",
]

# Output formats
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

# Language configuration
language = "en" if docset.endswith("_en") else "zh_CN"
locale_dirs = [f"{docset}/locale/"] if os.path.exists(f"{docset}/locale") else []
gettext_compact = False

# HTML theme configuration
html_short_title = ""
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static", f"{docset}/_static"] if os.path.exists(f"{docset}/_static") else ["_static"]
html_css_files = ["custom.css", "homepage.css"]
html_js_files = []
html_logo = "img/logo.png"
html_favicon = "img/logo.png"

# HTML theme options
html_theme_options = {
    "logo": {
        "text": multiproject_projects[docset]["config"]["project"],
    },
    "home_page_in_toc": True,
    "use_download_button": False,
    "repository_url": "https://github.com/flagos-ai/KernelGen",
    "use_repository_button": True,
    "secondary_sidebar_items": {
        "**": ["page-toc", "sourcelink"],
    },
    "footer_start": ["copyright"],
    "footer_end": [],
    "show_sphinx": False,
    "navbar_end": ["navbar-icon-links"]
}

html_context = {
    "default_mode": "dark",
    "current_project": docset,
    "project_title": multiproject_projects[docset]["config"]["project"],
}

# Sidebar configuration - customize per project if needed
html_sidebars = {
    "**": ["sidebar-nav-bs", "search-field"],
}

# RST epilog for common replacements
rst_epilog = """
.. |org_brand| replace:: KernelGen Community
.. |com_brand| replace:: KernelGen for Business
.. |git_providers_and| replace:: GitHub, Bitbucket, and GitLab
.. |git_providers_or| replace:: GitHub, Bitbucket, or GitLab
"""

autosectionlabel_prefix_document = True

# Linkcheck configuration
linkcheck_retries = 2
linkcheck_timeout = 1
linkcheck_workers = 10
linkcheck_ignore = [
    r"http://127\.0\.0\.1",
    r"http://localhost",
    r"https://github\.com.+?#L\d+",
]

# External links
extlinks = {
    "issue": ("https://github.com/armstrongttwalker-alt/test-i18n-KernelGen/issues/%s", "#%s"),
}

suppress_warnings = ["epub.unknown_project_files"]

# Print current configuration for debugging
print(f"INFO: Building project: {docset}")
print(f"INFO: Language: {language}")
print(f"INFO: Project title: {multiproject_projects[docset]['config']['project']}")
print(f"INFO: Exclude patterns: {exclude_patterns}")