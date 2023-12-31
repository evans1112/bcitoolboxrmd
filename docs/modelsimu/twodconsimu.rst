Two-Dimensional Continuous Simulation
~~~~~~~~~~

Introduction
--------

Users can use this function for two dimensional (**temporal** / **spatial** / **numerosity**) continuous simulation based on the BCI model.

Navigate
--------

**Main Menu** ---> **Model Simulation** ---> **Simulating for 2-D Continuous Condition**

Details
--------


.. image:: 2Dsimu.tif

1/2. **Parameters for each dimension**

 **pcommon**: The prior probability that both sensory information can be attributed to one cause.

 **sigma 1**: The standard deviation of the Gaussian distribution of the likelihood for modality 1.

 **sigma 2**: The standard deviation of the Gaussian distribution of the likelihood for modality 2.

 **sigmap**: The standard deviation of the Gaussian distribution of the prior.

 **mup**: The mean of the Gaussian distribution of the prior.

|

3/4. **Stimuli for each dimension**

Users can set the true stimuli.

|

5. **Elements**

 **Response Distribution**: Display the outputs of response distribution based on the prior and likelihood.

 **Stimulus Encoding**: Display the likelihoods of stimulus encoding.

 **Prior Distribution**: Display the distribution of prior expectation on the stimuli.

|


6. **Strategies**

 **Model Averaging**: Model averaging is when the observer weights the estimates of the stimulus locations by the inferred probabilities of their causal structure. Considered the most optimal strategy. See equation 15 in Wozny and Shams (2011).

 **Model Selection**: Model selection is when the observer selects the most likely causal structure and estimates the stimulus location wholly on the basis of the selected model. See equation 16 in Wozny and Shams (2011).

 **Probability Matching**: Probability matching is a strategy that choses the estimates from either causal structure based on their inferred probabilities. Although this method is suboptimal, it appears to be the most frequently used in cognitive tasks. See equation 17 in Wozny and Shams (2011).

|

7. **Estimates**

 **Peak**: Value indicated by red and blue diamonds.

 **Mean**: Value indicated by red and blue circles.

 **Display Value**: Display the value of the model estimate of probability on the figure.

|

**Simulate**

Click the button to generate the simulated results.

|

**Save the simulated data**

Click the button to save the simulated numerical data.
