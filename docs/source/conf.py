# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))#+os.sep+'seg1d')

# master_doc = 'source/index'

# -- Project information -----------------------------------------------------

project = 'seg1d'
copyright = '2020, Mathew Schwartz'
author = 'Mathew Schwartz'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.imgmath', 'numpydoc', 
              'sphinx.ext.intersphinx', 'sphinx.ext.coverage',
              'sphinx.ext.autosummary', 'matplotlib.sphinxext.plot_directive',
              'sphinx.ext.doctest']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -----------------------------------------------------------------------------
# Sphinx autodoc options
# -----------------------------------------------------------------------------

autoclass_content = 'class'
autodoc_member_order = 'groupwise'

# -----------------------------------------------------------------------------
# Autosummary
# -----------------------------------------------------------------------------

autosummary_imported_members = True
autosummary_generate = True
autosummary_generate_overwrite = True
numpydoc_show_class_members = False

# -- Try to auto-generate numba-decorated signatures -----------------

import numba
import inspect

default_role = "autolink"

def process_numba_docstring(app, what, name, obj, options, signature, return_annotation):
    if type(obj) is not numba.targets.registry.CPUDispatcher:
        return (signature, return_annotation)
    else:
        original = obj.py_func
        orig_sig = inspect.signature(original)

        if (orig_sig.return_annotation) is inspect._empty:
            ret_ann = None
        else:
            ret_ann = orig_sig.return_annotation.__name__

        return (str(orig_sig), ret_ann)

def setup(app):
    app.connect('autodoc-process-signature', process_numba_docstring)

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = 'scipy'
html_theme_path = ['_theme']

html_use_modindex = True
html_copy_source = False
html_domain_indices = False
html_file_suffix = '.html'

html4_writer = True

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
    "edit_link": "true",
    "sidebar": "right",
    "rootlinks": [("http://github.com/cadop/segment1d", "Github"),
                  ("http://", "Paper")]
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/devdocs', None),
    'scipy': ('https://scipy.github.io/devdocs', None),
    'matplotlib': ('https://matplotlib.org', None)
}

redirects_file = 'redirects.rst'

#------------------------------------------------------------------------------
# Plot style
#------------------------------------------------------------------------------

plot_pre_code = """
import numpy as np
import scipy as sp
np.random.seed(123)
"""
plot_include_source = True
plot_html_show_formats = False



# -----------------------------------------------------------------------------
# Source code links
# -----------------------------------------------------------------------------
import numpy
import inspect
from os.path import relpath, dirname

for name in ['sphinx.ext.linkcode', 'numpydoc.linkcode']:
    try:
        __import__(name)
        extensions.append(name)
        break
    except ImportError:
        pass
else:
    print("NOTE: linkcode extension not found -- no links to source generated")

def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    if domain != 'py':
        return None

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except Exception:
            return None

    # strip decorators, which would resolve to the source of the decorator
    # possibly an upstream bug in getsourcefile, bpo-1764286
    try:
        unwrap = inspect.unwrap
    except AttributeError:
        pass
    else:
        obj = unwrap(obj)

    try:
        fn = inspect.getsourcefile(obj)
    except Exception:
        fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        lineno = None

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""


    fn = relpath(fn, start='')

    return "https://github.com/cadop/segment1d/blob/master/seg1d/%s%s" % (
           fn, linespec)
    

from pygments.lexers import CLexer
import copy

class NumPyLexer(CLexer):
    name = 'NUMPYLEXER'

    tokens = copy.deepcopy(CLexer.tokens)
    # Extend the regex for valid identifiers with @
    for k, val in tokens.items():
        for i, v in enumerate(val):
            if isinstance(v, tuple):
                if isinstance(v[0], str):
                    val[i] =  (v[0].replace('a-zA-Z', 'a-zA-Z@'),) + v[1:]