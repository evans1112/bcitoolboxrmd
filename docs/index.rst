BCI Toolbox
===========

.. image:: _static/BCI.png
   :align: center
   :alt: BCI Toolbox logo
   :width: 55%

.. raw:: html

   <div class="hero-panel">
     <p class="hero-kicker">Bayesian Causal Inference for multisensory research</p>
     <p class="hero-copy">
       BCI Toolbox is a Python package and graphical workflow for fitting,
       simulating, visualizing, and exporting Bayesian causal inference models
       for behavioral data. It is designed for researchers who want a
       reproducible model pipeline without writing custom analysis code for
       every experiment.
     </p>
   </div>

.. image:: https://img.shields.io/badge/python-3.6%2B-blue
   :alt: Python 3.6+

.. image:: https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-informational
   :alt: Cross-platform

.. image:: https://img.shields.io/badge/interface-GUI%20%2B%20Python%20API-success
   :alt: GUI and API

What You Can Do
---------------

* Fit behavioral datasets with discrete or continuous responses.
* Compare model-averaging, model-selection, and probability-matching decision strategies.
* Build models with any number of modalities and one or more stimulus dimensions.
* Fit individual participants or grouped datasets and export reproducible results.
* Run parameter recovery, diagnostics, posterior-predictive checks, and model comparison.
* Use the graphical interface for import, fitting, plotting, and export.
* Use the v0.3.0 Python API for reproducible scripts and advanced workflows.

Recommended Reading Path
------------------------

To fit your own behavioral data from Python, start with the
:doc:`programmatic/quickstart`. For the graphical workflow, open
:doc:`installation` and then :doc:`basic_usage/gui`. If your experiment
contains two task dimensions, such as numerosity and time, continue with
:doc:`basic_usage/gui2d`.

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   open_tutorial
   programmatic/index
   basic_usage/index
   modelfit/index
   modelsimu/index

Citation
--------

If BCI Toolbox supports your work, please cite:

Zhu, H., Beierholm, U., & Shams, L. (2024). BCI Toolbox: An open-source
python package for the Bayesian causal inference model. PLOS Computational
Biology, 20(7), e1011791. https://doi.org/10.1371/journal.pcbi.1011791

For the 2D BCI module, please also cite:

Zhu, H., Zhang, Y., Beierholm, U., & Shams, L. (2026). Crossmodal interaction
of flashes and beeps across time and number follows Bayesian causal inference.
Psychonomic Bulletin & Review, 33, 58. https://doi.org/10.3758/s13423-026-02857-z

Contributors
------------

Haocheng Zhu, Dr. Ulrik R. Beierholm, and Dr. Ladan Shams.

Questions and feedback are welcome at evanszhu2001@gmail.com.
