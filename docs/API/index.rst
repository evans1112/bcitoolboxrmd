API
===

The Python API is useful when analyses need to be scripted, versioned, or run
outside the graphical interface.

Common entry points:

``bcitoolbox.gui()``
   Launch the standard GUI.

``bcitoolbox.gui2d()``
   Launch the 2D GUI.

``bcitoolbox.simulateVV(...)``
   Run the classic one-dimensional BCI simulation.

``bcitoolbox.fit(...)``
   Fit the classic BCI model.

``bcitoolbox.fit_2d_bci(...)``
   Fit a 2D BCI model from a parsed 2D dataset.

``bcitoolbox.simulate_2d_bci(...)``
   Simulate 2D BCI predictions for a dataset matrix.

.. toctree::
   :maxdepth: 2

   simulation
   simulation2d
