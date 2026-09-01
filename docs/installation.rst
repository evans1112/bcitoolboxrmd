Installation
============

BCI Toolbox is distributed as a Python package. The graphical interface uses
Tkinter, which is included with most standard Python installations.

Quick Install
-------------

Open a terminal and run:

.. code-block:: bash

   pip install bcitoolbox

Then verify the installation:

.. code-block:: python

   import bcitoolbox as btb
   print(btb.__name__)

Open the Tutorial
-----------------

.. include:: _includes/open_tutorial_steps.rst

Launching the GUI
-----------------

Standard GUI:

.. code-block:: python

   import bcitoolbox as btb
   btb.gui()

2D GUI:

.. code-block:: python

   import bcitoolbox as btb
   btb.gui2d()

Recommended Environment
-----------------------

Use a clean virtual environment when possible:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install bcitoolbox

On Windows, activate the environment with:

.. code-block:: bat

   .venv\Scripts\activate

Dependencies
------------

The package depends on common scientific Python libraries including NumPy,
SciPy, Matplotlib, pandas, scikit-learn, requests, and pyvbmc. The default
Powell optimizer works after the standard installation. VBMC fitting requires
``pyvbmc`` to be importable in the active Python environment.

Troubleshooting
---------------

If the GUI does not open, first confirm that Python can import Tkinter:

.. code-block:: python

   import tkinter
   tkinter.Tk()

If this raises an error, install a Python distribution that includes Tkinter
or add the platform-specific Tk package for your system.
