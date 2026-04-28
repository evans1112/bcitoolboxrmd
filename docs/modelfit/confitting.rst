Continuous Fitting
==================

Introduction
------------

Use continuous fitting when participants report freely on a continuous
stimulus scale rather than selecting one of several predefined response
categories. Typical examples include spatial localization, temporal estimates,
or other perceptual reports measured on a continuous axis.

Navigate
--------

**Main Menu** ---> **Model Fitting** ---> **Fitting for Continuous Data**


Details
-------

.. image:: confit.tif

1. **Import / Open file**

Users can upload one or more CSV files through *Import* or *Open file*. Batch
selection is recommended when the same model configuration will be applied to
multiple participants or sessions.

 The selected files containing behavioral data must be .csv files and need to be in the following format:


 +-----------------------+-----------------------+---------------------------+---------------------------+ 
 |True sti of modality 1 |True sti of modality 2 |Reported sti of modality 1 |Reported sti of modality 2 | 
 +-----------------------+-----------------------+---------------------------+---------------------------+
 |             ...       |...                    | ...                       | ...                       |
 +-----------------------+-----------------------+---------------------------+---------------------------+

|

2. **Number of simulations**

Number of samples for the probability distribution for each case. Users can set 1000 for testing and 10000 for final publication.

|

3. **Fit type**

The BCI toolbox provides several fit types, which is also how error (cost) is 
calculated:


 **mll**: Minus log likelihood

 **emd**: Earth mover's distance/Wasserstein distance

 **mr2**: Minus R square



Choose the objective that best matches the scientific goal and response
format.

|

4. **Decision Strategy**

The BCI toolbox provides three different decision strategies:


 **Model Averaging**: Model averaging is when the observer weights the estimates of the stimulus locations by the inferred probabilities of their causal structure. Considered the most optimal strategy. See equation 15 in Wozny and Shams (2011).

 **Model Selection**: Model selection is when the observer selects the most likely causal structure and estimates the stimulus location wholly on the basis of the selected model. See equation 16 in Wozny and Shams (2011).

 **Probability Matching**: Probability matching is a strategy that choses the estimates from either causal structure based on their inferred probabilities. Although this method is suboptimal, it appears to be the most frequently used in cognitive tasks. See equation 17 in Wozny and Shams (2011).

Select at least one strategy. If more than one strategy is selected, the
toolbox fits each strategy and reports the best-fitting result.

|

5. **Parameters**

Users can set the target estimated parameters and set their ranges.


 **pcommon**: The prior probability that both sensory information can be attributed to one cause.

 **sigma 1**: The standard deviation of the Gaussian distribution of the likelihood for modality 1.

 **sigma 2**: The standard deviation of the Gaussian distribution of the likelihood for modality 2.

 **sigmap**: The standard deviation of the Gaussian distribution of the prior.

 **mup**: The mean of the Gaussian distribution of the prior.

 **s1**: A constant added to the mean of the Gaussian distribution for the likelihood for modality 1.

 **s2**: A constant added to the mean of the Gaussian distribution for the likelihood for modality 2.


.. image:: parameters_interface.tif

6. **Run**

After reviewing the data, objective, strategy, and parameter bounds, click
*Run* and wait for the fitting process to finish. The status panel updates
during optimization.

After the fitting is complete, the results of it will be presented in a new window. The user can browse the fitting results and click save to save the results as a .txt file.

|

7. **Plot**

Use *Plot* to inspect the model prediction against behavioral data for a
selected dataset.

|

8. **Figure Save**

Users can click save to save all fitting figures or RDMs to folder. 

|

9. **Main Page**

Go back to main page.

Examples
--------

Example datasets are available on GitHub:
https://github.com/evans1112/bcitoolbox/tree/main/test_dataset/continuous
