# -*- coding: utf-8 -*-
import sys
import os
import glob
import shutil
import datetime
import sphinx_rtd_theme
import sphinx_gallery
from sphinx_gallery.scrapers import figure_rst
from sphinx_gallery.sorting import FileNameSortKey
import gmt
from gmt import __version__, __commit__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "numpydoc",
    "nbsphinx",
    "gmt.sphinxext.gmtplot",
    'sphinx_gallery.gen_gallery',
]

# Autosummary pages will be generated by sphinx-autogen instead of sphinx-build
autosummary_generate = False

numpydoc_class_members_toctree = False

# intersphinx configuration
intersphinx_mapping = {
    # "python": ("https://docs.python.org/3/", None),
    # "numpy": ("https://docs.scipy.org/doc/numpy/", None),
    # "pandas": ("http://pandas.pydata.org/pandas-docs/stable/", None),
    # "xarray": ("http://xarray.pydata.org/en/stable/", None),
}


class GMTScraper():

    def __init__(self):
        self.seen = set()

    def __call__(self, block, block_vars, gallery_conf):
        image_names = list()
        image_path_iterator = block_vars['image_path_iterator']
        for fig_name in gmt._figures:
            if fig_name not in self.seen:
                self.seen |= set(fig_name)
                fname = image_path_iterator.next()
                gmt._figures[fig_name].savefig(fname, transparent=True)
                image_names.append(fname)
        with open("/home/leo/src/gmt-python/meh.txt", "w") as f:
            f.write('\n')
            f.write(str(image_names))
            f.write('\n')
        return figure_rst(image_names, gallery_conf['src_dir'])


def gmt_scraper(block, block_vars, gallery_conf):
    """
    Parameters
    ----------
    block : tuple
        A tuple containing the (label, content, line_number) of the block.
    block_vars : dict
        Dict of block variables.
    gallery_conf : dict
        Contains the configuration of Sphinx-Gallery
    Returns
    -------
    rst : str
        The ReSTructuredText that will be rendered to HTML containing
        the images. This is often produced by
        :func:`sphinx_gallery.gen_rst.figure_rst`.
    """
    image_path_iterator = block_vars['image_path_iterator']
    image_paths = list()
    figures = [block_vars[k] for k in block_vars if isinstance(block_vars[k], Figure)]
    for fig, image_path in zip(figures, image_path_iterator):
        kwargs = dict(transparent=True)
        fig.savefig(image_path, **kwargs)
        image_paths.append(image_path)
    return figure_rst(image_paths, gallery_conf['src_dir'])


sphinx_gallery_conf = {
    # path to your examples scripts
    'examples_dirs': ['../examples'],
    # path where to save gallery generated examples
    'gallery_dirs': ['gallery'],
    'filename_pattern': r'\.py',
    # Remove the "Download all examples" button from the top level gallery
    'download_all_examples': False,
    # Sort gallery example by file name instead of number of lines (default)
    'within_subsection_order': FileNameSortKey,
    # directory where function granular galleries are stored
    'backreferences_dir': 'api/generated/backreferences',
    # Modules for which function level galleries are created.  In
    # this case sphinx_gallery and numpy in a tuple of strings.
    'doc_module': 'gmt',
    # Insert links to documentation of objects in the examples
    'reference_url': {'gmt': None},
    'image_scrapers': (GMTScraper(),),
}

# Sphinx project configuration
templates_path = ["_templates"]
exclude_patterns = ["_build", "**.ipynb_checkpoints"]
source_suffix = ".rst"
# The encoding of source files.
source_encoding = "utf-8-sig"
master_doc = "index"

# General information about the project
year = datetime.date.today().year
project = u"GMT/Python"
copyright = u"2017-2018, Leonardo Uieda and Paul Wessel"
if len(__version__.split("+")) > 1 or __version__ == "unknown":
    version = "dev"
else:
    version = __version__

# These enable substitutions using |variable| in the rst files
rst_epilog = """
.. |year| replace:: {year}
""".format(
    year=year
)

html_last_updated_fmt = "%b %d, %Y"
html_title = "GMT/Python"
html_short_title = "GMT/Python"
html_logo = "_static/gmt-python-logo.png"
html_favicon = "_static/favicon.png"
html_static_path = ["_static"]
html_extra_path = [".nojekyll", "CNAME"]
pygments_style = "default"
add_function_parentheses = False
html_show_sourcelink = False
html_show_sphinx = True
html_show_copyright = True

# Theme config
html_theme = "sphinx_rtd_theme"
html_theme_options = {}
html_context = {
    "menu_links": [
        ('<i class="fa fa-play fa-fw"></i> Try it online!', "http://try.gmtpython.xyz"),
        (
            '<i class="fa fa-github fa-fw"></i> Source Code',
            "https://github.com/GenericMappingTools/gmt-python",
        ),
        (
            '<i class="fa fa-users fa-fw"></i> Contributing',
            "https://github.com/GenericMappingTools/gmt-python/blob/master/CONTRIBUTING.md",
        ),
        (
            '<i class="fa fa-book fa-fw"></i> Code of Conduct',
            "https://github.com/GenericMappingTools/gmt-python/blob/master/CODE_OF_CONDUCT.md",
        ),
        (
            '<i class="fa fa-gavel fa-fw"></i> License',
            "https://github.com/GenericMappingTools/gmt-python/blob/master/LICENSE.txt",
        ),
        (
            '<i class="fa fa-comment fa-fw"></i> Contact',
            "https://gitter.im/GenericMappingTools/gmt-python",
        ),
    ],
    # Custom variables to enable "Improve this page"" and "Download notebook"
    # links
    "doc_path": "doc",
    'galleries': sphinx_gallery_conf['gallery_dirs'],
    'gallery_dir': dict(zip(sphinx_gallery_conf['gallery_dirs'],
                            sphinx_gallery_conf['examples_dirs'])),
    "github_repo": "GenericMappingTools/gmt-python",
    "github_version": "master",
}


# Load the custom CSS files (needs sphinx >= 1.6 for this to work)
def setup(app):
    app.add_stylesheet("style.css")
