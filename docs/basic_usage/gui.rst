Graphical User Interface (GUI)
=============

.. tabs::

   .. tab:: Import and call
      :ref:`I_C`

   .. tab:: Fitting module
      :ref:`F_M`

.. _I_C:

**Import and call**

.. code-block:: bash

      import bcitoolbox as btb

.. code-block:: bash

      btb.gui()

.. _F_M:

**Fitting module**

.. image:: image.gif

1. Import / Open file

Users can upload single or multiple files simultaneously via either *Import* or *Open file*. Users can also add the file paths to the entry box and click *Import* to upload.

The selected files containing behavioral data must be .csv files and need to be in the following format:

(True number of stimuli from modality U)	(True number of stimuli from modality D)	(Reported number of stimuli from modality U)	(Reported number of stimuli from modality D)
...	...	...	...

2. Number of simulations

Number of samples for the probability distribution for each case. Users can choose 1000 for testing and 10000 for final publication.

3. Fit type

The BCI toolbox provides three fit types, which is also how errors are 
calculated:

*mll*: Minus log likelihood
*mr2*: Minus R square
*sse*: Sum of Squares for Errors

Users can select any one of it depending on specific condition.

4. Decision Strategy

The BCI toolbox provides three different decision strategies:


