# `bcitoolbox.recovery` — validation tools

Two questions every model-based analysis should answer before its parameters
are believed.

| Question | Tool |
| --- | --- |
| Can this design recover the parameters at all? | [`recover`](#recover) |
| Does the fitted model actually reproduce the data? | [`posterior_predictive`](#posterior_predictive) |
| Did this particular fit go wrong? | [`Fit.diagnostics`](#fitdiagnostics) |

---

## `recover`

```python
recover(model, conditions, vary=None, truths=None, n_datasets=20, n_trials=50,
        fit_model=None, seed=0, progress=None, **fit_kwargs) -> RecoveryResult
```

Generate data from known parameters, fit them back, and report how well each
one is recovered.

| Parameter | Type | Description |
| --- | --- | --- |
| `model` | `Model` | Generating model. Its response models must be configured — a discrete one needs explicit `levels`, since no data exist yet. |
| `conditions` | array or `Data` | Conditions to simulate, in any form `Model.simulate` accepts. |
| `vary` | `dict` | `{parameter: (low, high)}` ranges to draw true values from. A plain number holds that parameter constant. |
| `truths` | `list[dict]` | Explicit generating parameters, one dict per data set. Overrides `vary` and `n_datasets`. |
| `n_datasets` | `int` | Number of data sets. **20 or more** before reading much into an r². |
| `n_trials` | `int` | Simulated trials per condition in each data set. |
| `fit_model` | `Model` | Model used for fitting. Defaults to a copy of `model` with every varied parameter freed — pass a different one to study model misspecification. |
| `seed` | `int` | Seed for the drawn parameters and the simulations. |
| `**fit_kwargs` | | Passed to `Model.fit`, e.g. `n_sim=2000`. |

**Returns:** `RecoveryResult`

| Member | Description |
| --- | --- |
| `pairs` | `(truth, fit)` tuples — the format `btb.plot.recovery` expects. |
| `to_frame()` | Long frame: `dataset, parameter, true, estimated`. |
| `summary()` | Per parameter: `r2`, `bias`, `mae`, `rmse`, and `rmse_relative` (rmse over the range of the true values, which makes parameters on different scales comparable). |
| `plot()` | True against estimated, one panel per parameter. |

```python
result = btb.recover(generator, conditions,
                     vary={"p_common": (0.1, 0.9),
                           "sigma_visual": (1.0, 5.0),
                           "sigma_auditory": (4.0, 14.0)},
                     n_datasets=20, n_trials=60, n_sim=2000)
print(result.summary())
result.plot()
```

**How many trials do I need?** Run the same call at several `n_trials` and watch
`rmse_relative` fall:

```python
for n in (20, 40, 80, 160):
    result = btb.recover(generator, conditions, vary=vary, n_trials=n, n_sim=1500)
    print(n, result.summary().set_index("parameter")["rmse_relative"].round(3).to_dict())
```

---

## `posterior_predictive`

```python
posterior_predictive(fit, statistic="mean", n_replicates=200, n_sim=None,
                     seed=0, dimension=None) -> PosteriorPredictive
```

Simulate replicate data sets **of exactly the same size** as the real one from
the fitted parameters, and check whether the observed summary statistics fall
inside the resulting predictive distributions. A model can have an excellent
likelihood and still miss an obvious feature of the data; this is what catches
it.

| Parameter | Description |
| --- | --- |
| `fit` | A `Fit` with data attached. |
| `statistic` | `"mean"` or `"sd"` of the responses in each cell. |
| `n_replicates` | Number of replicate data sets. |
| `n_sim` | Simulated trials in the underlying pool (default `50 × n_replicates`, capped at 20000). |
| `dimension` | Dimension to check; defaults to the first reported one. |

**Returns:** `PosteriorPredictive`

| Member | Description |
| --- | --- |
| `frame` | One row per cell: `observed`, `predicted_mean`, `lower`, `upper`, `inside`, `z`. |
| `coverage` | Fraction of cells inside their 95% interval. |
| `mean_abs_z`, `max_abs_z` | Mean and maximum standardised discrepancy. |
| `summary()` | Printable verdict, listing the worst-missed cells. |
| `plot()` | Observed against predicted, with intervals. |

> **Read `mean_abs_z`, not just `coverage`.** Coverage only counts cells in or
> out, so a model can keep most cells inside a wide interval while sitting
> several standard deviations away in the cells that matter. On a localisation
> data set, the correct model gives coverage 96.9% and mean |z| 0.71; a model
> forced never to integrate gives coverage 75.0% and mean |z| 1.58, with every
> badly-missed cell being an auditory one — exactly the modality that should
> have been pulled by vision.

---

## `Fit.diagnostics`

```python
fit.diagnostics(tolerance=0.01, spread=0.1) -> dict
```

Checks three things that go wrong often enough to be worth automating:

1. **An estimate sits on its bound** — either the bound is too tight, or the
   parameter is running away because the data do not constrain it.
2. **Different starting points reach the same objective with different
   parameters** — the design cannot identify that parameter, or that
   combination of parameters.
3. **Different starting points reach different objectives** — local minima, or
   simulation noise that is too large.

Checks 2 and 3 need `n_start > 1`. Returns `{"issues", "text", "ok"}`; any
issues are also printed by `fit.summary()`.

```python
fit = model.fit(data, n_start=4)
print(fit.diagnostics()["text"])
```

A real example. In a rubber-hand experiment where the only response is a
symmetric yes/no ownership judgement, the two sensory noises enter the model
almost entirely through their **sum**:

```
Diagnostics for rhi: 1 issue(s)
  [not_identified] These parameters reached the same objective from different
  starting points with very different values: sigma_visual_time,
  sigma_tactile_time. This design does not identify them separately - fix one,
  tie them together, or add a condition that separates them.
```

Three starting points illustrate the point — the same objective, wildly
different splits, and an almost constant sum of squares:

| error | `sigma_visual_time` | `sigma_tactile_time` | sum of squares |
| --- | --- | --- | --- |
| 1729.1 | 147.8 | 121.2 | 36551 |
| 1744.0 | 217.8 | 49.7 | 49923 |
| 1744.3 | 84.3 | 199.4 | 46871 |

Tying them resolves it, and the tied value recovers the true combination:

```python
model.tie("sigma_tactile_time", "sigma_visual_time")
```
