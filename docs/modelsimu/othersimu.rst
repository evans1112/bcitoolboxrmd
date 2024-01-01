Specific Simulation (s)
~~~~~~~~~~

Introduction
--------

Users can use this simulation function for some specific cognitive tasks (numerosity task,...coming soon) based on the BCI model.

Navigate
--------

**Main Menu** ---> **Model Simulation** ---> **Simulating for numerosity task**

Details
--------


.. image:: othersimu.tif

1. **Parameters**

 **pcommon**: The prior probability that both sensory information can be attributed to one cause.

 **sigma 1**: The standard deviation of the Gaussian distribution of the likelihood for modality 1.

 **sigma 2**: The standard deviation of the Gaussian distribution of the likelihood for modality 2.

 **sigmap**: The standard deviation of the Gaussian distribution of the prior.

 **mup**: The mean of the Gaussian distribution of the prior.

|

2. **Number of stimuli**

Users can set the true max number of stimuli in the numerosity task.

|


3. **Strategies**

 **Model Averaging**: Model averaging is when the observer weights the estimates of the stimulus locations by the inferred probabilities of their causal structure. Considered the most optimal strategy. See equation 15 in Wozny and Shams (2011).

 **Model Selection**: Model selection is when the observer selects the most likely causal structure and estimates the stimulus location wholly on the basis of the selected model. See equation 16 in Wozny and Shams (2011).

 **Probability Matching**: Probability matching is a strategy that choses the estimates from either causal structure based on their inferred probabilities. Although this method is suboptimal, it appears to be the most frequently used in cognitive tasks. See equation 17 in Wozny and Shams (2011).

|


**Simulate**

Click the button to generate the simulated results.

|

**Save the simulated data**

Click the button to save the simulated numerical data.
