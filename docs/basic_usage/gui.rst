Graphical User Interface
========================

The BCI Toolbox GUI provides a complete no-code workflow for model fitting,
simulation, visualization, and export. It is useful for rapid model checking,
batch fitting across participant files, and communicating results with
publication-ready figures.

Launch
------

.. code-block:: python

   import bcitoolbox as btb
   btb.gui()

Main Workflows
--------------

Model fitting
   Import one or more CSV files, choose the fitting objective, select one or
   more decision strategies, estimate parameters, inspect plots, and export
   results.

Model simulation
   Enter parameter values and stimulus conditions to generate model-predicted
   response distributions. The simulation tools are useful for understanding
   how priors, likelihood variance, and causal-prior assumptions shape
   behavior.

Typical Analysis Workflow
-------------------------

1. Prepare a CSV file with one row per trial.
2. Open the GUI and select the relevant fitting module.
3. Import one or more datasets.
4. Set the simulation count. Use a smaller value, such as ``1000``, for a
   quick pilot run and a larger value, such as ``10000``, for final fitting.
5. Choose the objective function and decision strategies.
6. Select free parameters and review bounds.
7. Run fitting and inspect the output log.
8. Plot the fitted model against behavioral data.
9. Save figures, RDMs, predictions, or parameter summaries as needed.

Decision Strategies
-------------------

``ave``
   Model averaging. The observer weights causal-structure-specific estimates
   by the posterior probability of a common cause.

``sel``
   Model selection. The observer uses the estimate from the most likely causal
   structure.

``mat``
   Probability matching. The observer samples a causal structure according to
   the posterior probability and responds from that structure.

Fitting Objectives
------------------

``mll``
   Minus log likelihood. Recommended for discrete response distributions when
   likelihood-based model comparison is desired.

``mr2`` or ``minusr2``
   Negative squared correlation between model and behavioral response
   proportions.

``sse``
   Sum of squared errors between model and behavioral response proportions.

``emd``
   Earth mover's distance, available for selected continuous workflows.

When to Use the 2D GUI
----------------------

Use :doc:`gui2d` when each trial contains two stimulus dimensions. For
example, a flash-beep experiment may require both numerosity values and
temporal offsets. The 2D GUI keeps these dimensions in one model instead of
fitting separate one-dimensional analyses.
