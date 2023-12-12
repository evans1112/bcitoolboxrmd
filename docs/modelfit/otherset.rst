Other Settings
~~~~~~~~~~

Introduction
------------
Here we can configure some specific settings for the fitting


Navigate
--------

**Main Menu** ---> **Model Fitting** ---> **Settings**


Details 
--------

.. image:: other.tif

1. **Number of seeds**

Set up the number of random seeds.

2. **Fitting methods**

Set up the parameters optimization methods.

 `Powell <https://en.wikipedia.org/wiki/Powell%27s_method>`_ : a method for finding a minimum of a function without the need for gradient information, relying on a set of directions to minimize along and updating them based on function evaluations.

 `VBMC <https://github.com/acerbilab/vbmc>`_ : is an approximate inference method designed to fit and evaluate computational models with a limited budget of potentially noisy likelihood evaluations (e.g., for computationally expensive models).




Suggestions: Users can use the Powell algorithm for faster fitting, more random seeds or the VBMC algorithm for more accurate results (which is **more time consuming**).

