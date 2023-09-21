Simulation
~~~~~~~~~~

.. module:: https://github.com/evans1112/bcitoolboxrmd/tree/67b2b62683a61e180671e533b055319aee7e774e/docs/API/module/BCIbox.py
   :synopsis: This module provides utilities for data processing.

.. autofunction:: BCIbox.simulateVV

   :param data: The input data to be processed.
   :type data: list
   :param operation: The operation to apply to the data (e.g., 'sum', 'average').
   :type operation: str
   :returns: The result of the data processing.
   :rtype: float

   This function processes input data by applying a specified operation.


`btb.simulateVV (parameters, n_simulation, behavior_data, biOnly = True, strategy = 'ave' , fit_type = 'mll')` 
-----------------------------------------

:parameters: `array, float` An array, [pcommon, sigmaU, sigmaD [, sigmap, mup, sU, sD]].
:n_simulation: `int` Number of simulations for each condition.
:behavior_data: `array, int`  A n*4 array, see below for details:

:biOnly: `bool, optional`  If True use only bisensory conditions to calculate errors. It finds a solution that combines stability and recency, by default True. If False use all conditions to calculate errors.
:Strategy: `string, optional` ‘ave’ for model averaging; ‘sel’ for model selection; ‘mat’ for probability matching ; Default: ‘ave’

:fit_type: `string, optional`  ‘mll’ for minus log likelihood; ‘mr2’ for minus R square; ‘sse’ for sum of squares for errors; Default: ‘mll’

