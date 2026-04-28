2D API
======

The 2D API mirrors the 2D GUI workflow and is intended for reproducible
analysis scripts.

Launch the Interface
--------------------

.. code-block:: python

   import bcitoolbox as btb
   btb.gui2d()

Read a 2D CSV
-------------

.. code-block:: python

   from bcitoolbox.bci2d import read_csv_2d

   data = read_csv_2d(
       "participant_01.csv",
       stim_v_col="Flash",
       stim_a_col="Beep",
       time_col="SOA",
       resp_v_col="R_F",
       resp_a_col="R_B",
       soa_mode="visual_minus_auditory",
   )

For two modality-specific secondary columns, pass ``time_v_col`` and
``time_a_col`` instead of a single ``time_col``.

Fit a 2D Model
--------------

.. code-block:: python

   from bcitoolbox.bci2d import fit_2d_bci

   best, all_seed_results = fit_2d_bci(
       data,
       n_sim=10000,
       n_seeds=3,
       strategy="ave",
       fit_type="mll",
       method="Powell",
   )

``best`` is a dictionary containing the selected parameters, objective value,
strategy, seed, simulation output, and likelihood-based criteria when
available.

Select Free Parameters
----------------------

Use ``free_mask`` to choose which parameters are estimated. Use
``fixed_values`` for values held constant.

.. code-block:: python

   free_mask = [
       True,   # p_common
       True,   # sigma modality 1 primary
       True,   # sigma modality 2 primary
       False,  # sigma modality 1 secondary
       False,  # sigma modality 2 secondary
       True,   # sigma prior primary
       True,   # mu prior primary
       False,  # sigma prior secondary
       False,  # mu prior secondary
       False,  # bias modality 1
       False,  # bias modality 2
   ]

   best, _ = fit_2d_bci(data, free_mask=free_mask)

Simulate One Condition
----------------------

.. code-block:: python

   from bcitoolbox.bci2d import simulate_2d_condition

   params = [0.5, 0.4, 0.8, 60, 40, 2, 1, 400, 0, 0, 0]
   result = simulate_2d_condition(
       params,
       n_sim=10000,
       condition=(1, 2, 0, 150),
       strategy="ave",
   )

The returned dictionary includes modality-specific 2D response points and can
be used for custom plotting.

Export Predictions
------------------

.. code-block:: python

   from bcitoolbox.bci2d import save_prediction_csv

   save_prediction_csv(
       best,
       "participant_01_2d_predictions.csv",
       modality_names=["Visual", "Auditory"],
       dimension_labels={"primary": "numerosity", "secondary": "time"},
   )

Parameter Order
---------------

.. code-block:: text

   p_common
   sigma_v_number
   sigma_a_number
   sigma_v_time
   sigma_a_time
   sigma_number_prior
   mu_number_prior
   sigma_time_prior
   mu_time_prior
   bias_v
   bias_a
