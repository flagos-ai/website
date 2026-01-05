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
   $ PROJECT=flagos_zh make html  # build the Chinese project
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

# Define all projects with their configurations
multiproject_projects = {
    "flagos_en": {
        "use_config_file": False,
        "config": {
            "project": "Documentation",
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

docset = get_project(multiproject_projects)

ogp_site_name = "KernelGen Documentation"
ogp_use_first_image = True
ogp_image = "https://docs.readthedocs.io/en/latest/_static/img/logo-opengraph.png"
ogp_custom_meta_tags = (
    '<meta name="twitter:card" content="summary_large_image" />',
)
ogp_enable_meta_description = True
ogp_description_length = 300

# templates_path = ["_templates"]
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")

master_doc = "index"
copyright = '2025, FlagOS Community'
author = 'FlagOS Community'
release = '1.0.0'
# release = version

# Exclude patterns - exclude all other project directories
exclude_patterns = ["_build", "shared", "_includes"]
all_projects = list(multiproject_projects.keys())
for project in all_projects:
    if project != docset:
        exclude_patterns.append(project)

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

# Set language based on project suffix
language = "en" if docset.endswith("_en") else "zh_CN"

locale_dirs = [
    f"{docset}/locale/",
]
gettext_compact = False

html_short_title = ""

# ============================================================================
# HTML THEME CONFIGURATION - DIFFERENT THEMES FOR DIFFERENT PROJECTS
# ============================================================================

# Only flagos_en and flagos_zh use pydata_sphinx_theme, all others use sphinx_book_theme
if docset in ["flagos_en", "flagos_zh"]:
    html_theme = "pydata_sphinx_theme"
else:
    html_theme = "sphinx_book_theme"

# Common static paths
html_static_path = ["_static", f"{docset}/_static"]
html_css_files = ["custom.css", "homepage.css"]
html_js_files = []

html_logo = "img/logo.png"
html_favicon = "img/logo.png"

# Theme-specific configurations
if html_theme == "pydata_sphinx_theme":
    # PyData Sphinx Theme configuration for flagos_en and flagos_zh
    html_theme_options = {
        "logo": {
            "text": "Documentation",
        },
        "home_page_in_toc": True,
        "use_download_button": False,
        "repository_url": "https://github.com/flagos-ai/KernelGen",
        "use_repository_button": True,
        "secondary_sidebar_items": {},
        "footer_start": ["copyright"],
        "footer_end": [],
        "show_sphinx": False,
        "navbar_end": ["navbar-icon-links"]
    }
    
    # Update secondary sidebar items for flagos projects
    for project in ["flagos_en", "flagos_zh"]:
        html_theme_options["secondary_sidebar_items"][f"{project}/index"] = []
    
    # html_sidebars is only for PyData Sphinx Theme
    html_sidebars = {}
    for project in all_projects:
        html_sidebars[f"{project}/index"] = []
    
    # html_context is only applied to PyData Sphinx Theme
    html_context = {
        "default_mode": "dark"
    }

else:
    # Sphinx Book Theme configuration for all other projects

    # # repo URL per project
    # repository_urls = {
    #     "flagcx_en": "https://github.com/flagos-ai/FlagCX",
    #     "flagcx_zh": "https://github.com/flagos-ai/FlagCX",
    #     "flaggems_en": "https://github.com/flagos-ai/FlagGems",
    #     "flaggems_zh": "https://github.com/flagos-ai/FlagGems",
    #     "flagtree_en": "https://github.com/flagos-ai/FlagTree",
    #     "flagtree_zh": "https://github.com/flagos-ai/FlagTree",
    #     "flagrelease_en": "https://github.com/flagos-ai/FlagRelease",
    #     "flagrelease_zh": "https://github.com/flagos-ai/FlagRelease",
    #     "flagperf_en": "https://github.com/flagos-ai/FlagPerf",
    #     "flagperf_zh": "https://github.com/flagos-ai/FlagPerf",
    # }
    
    # # Obtain the current repo URL, if failed, set the default value
    # current_repo_url = repository_urls.get(docset, "https://github.com/flagos-ai")

    if docset.endswith("_en"):
        main_site_url = "https://docs.flagos.io/en/latest/"
        main_site_text = "Back to FlagOS Documentation"
    else:
        main_site_url = "https://docs.flagos.io/zh/latest/"
        main_site_text = "返回 FlagOS 文档"

    templates_path = ["_templates"]

    # Sphinx Book Theme configuration for all other projects
    html_theme_options = {
        "logo": {
            "image_light": "_static/dark-logo.svg",
            "image_dark": "_static/light-logo.svg",
        },
        "home_page_in_toc": True,
        "use_download_button": False,
        "repository_url": "https://github.com/flagos-ai/website",
        "use_edit_page_button": True,
        "use_repository_button": True,
        "navbar_center": ["back_to_main.html"],
        }

    html_context = {
        "main_site_url": main_site_url,
        "main_site_text": main_site_text,
    }

    # No html_sidebars for Sphinx Book Theme
    html_sidebars = {}
    # No html_context for Sphinx Book Theme
    html_last_updated_fmt = '%b %d, %Y %H:%M'

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