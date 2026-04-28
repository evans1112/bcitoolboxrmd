Model Simulation
================

Simulation is useful for understanding the behavior of the BCI model before
fitting data, diagnosing fitted parameters, and creating predicted response
distributions for specific stimulus conditions.

The toolbox includes:

One-dimensional continuous simulation
   Simulate a single stimulus dimension such as time, space, or numerosity.

Two-dimensional continuous simulation
   Simulate paired dimensions, such as numerosity plus time. For the newer
   integrated 2D GUI workflow, see :doc:`../basic_usage/gui2d`.

Discrete simulation
   Simulate response proportions over discrete response categories.

Other task simulations
   Additional task-specific simulation tools.

.. toctree::
   :maxdepth: 2

   onedconsimu
   twodconsimu
   discsimu
   othersimu
