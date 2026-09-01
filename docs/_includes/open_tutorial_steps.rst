BCI Toolbox 0.3.0 includes an end-to-end tutorial notebook with packaged and
simulated data. The commands below make an editable copy and open it in
JupyterLab.

Create a clean analysis folder and virtual environment.

On macOS or Linux:

.. code-block:: bash

   mkdir my-bci-analysis
   cd my-bci-analysis
   python3 -m venv .venv
   source .venv/bin/activate

On Windows PowerShell:

.. code-block:: powershell

   mkdir my-bci-analysis
   cd my-bci-analysis
   py -m venv .venv
   .venv\Scripts\Activate.ps1

Install the toolbox and JupyterLab:

.. code-block:: bash

   python -m pip install "bcitoolbox==0.3.0" jupyterlab

Copy the notebook from the installed package into the current folder, then
open it:

.. code-block:: bash

   python -c "import bcitoolbox as btb; print(btb.copy_tutorial('.'))"
   python -m jupyterlab bcitoolbox_tutorial.ipynb

JupyterLab opens ``bcitoolbox_tutorial.ipynb`` in the browser. If it asks for
a kernel, select the Python interpreter from ``.venv``, then choose
**Run → Run All Cells**. No data file is required for the first run.

If ``bcitoolbox_tutorial.ipynb`` already exists, open that copy directly. To
replace it with a fresh copy, save any work you want to keep and run:

.. code-block:: python

   import bcitoolbox as btb
   btb.copy_tutorial(".", overwrite=True)
