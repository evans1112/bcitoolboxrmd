# `bcitoolbox.results` — fits, groups and simulations

Nothing in this module performs modelling; these objects hold outcomes and know
how to display, export and compare them.

---

## `Fit`

Returned by `Model.fit`.

### Attributes

| Attribute | Type | Description |
| --- | --- | --- |
| `values` | `dict` | Fitted parameter values, including the fixed ones. |
| `error` | `float` | Objective value at the optimum (always minimised). |
| `objective` | `str` | Objective used. |
| `strategy` | `str` | Winning decision strategy. |
| `log_likelihood`, `aic`, `bic` | `float` | Information criteria; `NaN` for objectives not on the likelihood scale. |
| `r2` | `float` | Coefficient of determination between predicted and observed response distributions. |
| `n_observations` | `int` | Number of scored responses. |
| `n_free` | `int` | Number of estimated parameters. |
| `model` | `Model` | A **copy** of the model with fitted values — your original model is untouched. |
| `data` | `Data` | The fitted data set. |
| `strategy_comparison` | `list[dict]` | One entry per strategy tried: strategy, error, log likelihood, AIC, BIC. |
| `optimization` | `OptimizationResult` | Full optimiser output, including every starting point. |

`fit["p_common"]` is shorthand for `fit.values["p_common"]`.
`fit.free_values` returns only the estimated parameters.

### Methods

| Method | Description |
| --- | --- |
| `summary()` / `print_summary()` | Multi-line report: strategy, objective, information criteria, convergence, strategy comparison, any diagnostic warnings, and the parameter table. |
| `diagnostics(tolerance=0.01, spread=0.1)` | Check for estimates on their bounds, unidentified parameters and local minima. See [`recovery.md`](recovery.md#fitdiagnostics). |
| `to_frame()` | Parameter table as a `DataFrame`. |
| `predict(n_sim=None)` | Predicted vs observed response distributions for the fitted data. |
| `posterior_predictive(...)` | Via `btb.posterior_predictive(fit)` — do the replicate data sets look like the real one? |
| `simulate(conditions=None, n=10000, seed=13)` | Simulate the fitted model; defaults to the fitted conditions. |
| `to_dict()` / `save(path)` | JSON-serialisable record / write it to disk. |

### Example

```
Fit: recovery_continuous
  strategy      : averaging
  objective     : mll = 6631.51
  log likelihood: -6631.51   AIC: 13273   BIC: 13302.3
  distribution r2: 0.966
  observations  : 2560   free parameters: 5
  optimizer     : powell, 590 evaluations, 14.1s
  starts        : 3 (consistent)
  strategies    : averaging=6631.51 *, selection=6702.3, matching=6688.1
```

---

## `FitGroup`

Returned by `Model.fit(data, by="subject")`. Behaves like a dictionary:
`group["s01"]`, `for name, fit in group.items()`, `len(group)`.

| Method | Description |
| --- | --- |
| `to_frame()` | One row per fit: every parameter plus strategy, error, log likelihood, AIC, BIC, r². |
| `summary()` / `print_summary()` | Group-level mean, SD and 95% CI of each free parameter, the count of winning strategies, and the summed BIC. |
| `save_csv(path)` | Write `to_frame()` to CSV. |

---

## `Simulation`

Returned by `Model.simulate`.

| Attribute | Shape | Description |
| --- | --- | --- |
| `conditions` | `(n_conditions, n_mod, n_dim)` | Simulated conditions. |
| `responses` | `(n_conditions, n_sim, n_mod, n_dim)` | Responses after motor noise, lapses and discretisation. |
| `estimates` | same | Perceptual estimates *before* the response mapping. |
| `p_common` | `(n_conditions, n_sim)` | Posterior probability of a common cause on each simulated trial. |
| `values` | `dict` | Parameter values used. |
| `strategy` | `str` | Decision strategy used. |

| Method | Description |
| --- | --- |
| `to_frame(include_estimates=False)` | Long `DataFrame`, one row per simulated trial. |
| `summary()` | Per-condition mean and SD of the responses, plus mean `p(C=1)`. |
| **`to_data(name="simulated")`** | Convert to a `Data` object, so the simulation can be fitted exactly like real data — the basis of parameter recovery and power analysis. |
| `save_csv(path, long_format=True)` | Write trials (`True`) or the per-condition summary (`False`). |

---

## `compare`

```python
compare(fits, criterion="bic") -> pandas.DataFrame
```

Compare fits **of the same data** under different models or strategies. Accepts
a list or a `{label: fit}` dict. Returns one row per fit with the criterion, its
difference from the best model, and the corresponding weights, sorted best
first.

A `FitGroup` may be passed as an entry: it is aggregated by **summing** the
criterion over its members, which is the right thing for independent
per-subject fits, and the reported strategy is the modal one.

```python
btb.compare({"causal inference": group_full, "no integration": group_null})
```

```python
>>> btb.compare({"BCI": fit_full, "no-integration": fit_null})
          model  strategy  n_free  log_likelihood      bic  delta_bic   weight
            BCI averaging       3        -1277.55  2576.91       0.00 1.00e+00
 no-integration averaging       2        -1372.46  2759.46     182.55 2.29e-40
```

Only fits obtained with a likelihood objective (`"mll"`) have meaningful
information criteria; other rows contain `NaN`.

---

## `load_fit`

```python
load_fit(path) -> dict
```

Read a JSON file written by `Fit.save`. Rebuild a runnable model with
`btb.Model.from_dict(record["model"])`.
