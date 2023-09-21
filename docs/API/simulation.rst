Simulation
~~~~~~~~~~


`btb.simulateVV` (parameters, n_simulation, behavior_data, biOnly = True, strategy = 'ave' , fit_type = 'mll')
-----------------------------------------

Inputs:

:parameters: `array, float` An array, [pcommon, sigmaU, sigmaD [, sigmap, mup, sU, sD]].
:n_simulation: `int` Number of simulations for each condition.
:behavior_data: `array, int`  A n*4 array, see below for details:

:biOnly: `bool, optional`  If True use only bisensory conditions to calculate errors. It finds a solution that combines stability and recency, by default True. If False use all conditions to calculate errors.
:Strategy: `string, optional` ‘ave’ for model averaging; ‘sel’ for model selection; ‘mat’ for probability matching ; Default: ‘ave’
:fit_type: `string, optional`  ‘mll’ for minus log likelihood; ‘mr2’ for minus R square; ‘sse’ for sum of squares for errors; Default: ‘mll’

Returns:

:error: `float` The error between model and behavioral data.
:modelprop: `array, float` An array of model proportions of each condition.
:dataprop: `array, float` An array of data proportions of each condition.   
:responsesSim: `array, float` An array of simulated responses.



`btb.fit` (n_parameters, n_simulation, behavior_data, n_seeds = 1, bounds = [(0, 1),(0.1, 3),(0.1, 3),(0.1,3),(0, 3.5)], biOnly = 1, strategies = ['ave'], fittype = 'mll')
-----------------------------------------

