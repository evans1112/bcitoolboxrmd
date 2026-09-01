# `bcitoolbox.likelihood` — objectives and information criteria

The unit of comparison is a **cell**: one (condition, modality, dimension)
combination that actually contains responses. A data set with 15 conditions,
two modalities and one reported dimension has up to 30 cells; unimodal
conditions and unreported modalities simply contribute fewer.

---

## Objectives

| Name | Aliases | Description | AIC/BIC? |
| --- | --- | --- | --- |
| `"mll"` | `nll`, `loglik`, `fre` | Minus log likelihood. Multinomial for discrete responses, Gaussian kernel density for continuous ones. **Default.** | yes |
| `"sse"` | `sumsq` | Sum of squared errors between predicted and observed response distributions. | no |
| `"r2"` | `mr2`, `minus_r2` | Minus the squared correlation between predicted and observed distributions. | no |
| `"emd"` | `wasserstein` | Earth mover's (Wasserstein) distance between predicted and observed response **samples**. | no |

`normalise_objective(name)` maps any alias to its canonical name.

> **On AIC and BIC.** Only `"mll"` lives on the likelihood scale, so only
> `"mll"` yields meaningful information criteria. Fits obtained with `"sse"`,
> `"r2"` or `"emd"` report `NaN` for `log_likelihood`, `aic` and `bic` rather
> than a number that looks usable but is not.

> **On `"emd"`.** The distance is computed between the observed and simulated
> response *samples*, which is the definition of the Wasserstein distance. The
> legacy GUI computed it between kernel *density values*, which is a different
> quantity; numbers from the two are not comparable.

---

## `ScoringPlan`

```python
ScoringPlan(data, response_models)
```

Pre-indexed view of a data set, ready to be scored. Extracting the cells is done
once, so an optimiser only pays for the model simulation on each iteration.

| Parameter | Description |
| --- | --- |
| `data` | A `Data` object. Its `conditions` define the conditions the model must simulate, in the same order. |
| `response_models` | One response model per stimulus dimension. Dimensions with no recorded response may be `None` and are skipped. |

| Attribute | Description |
| --- | --- |
| `cells` | `(condition_index, modality_index, dimension_index, observed_values)` for every non-empty cell. |
| `n_observations` | Total number of scored responses — the `n` in BIC. |

### `evaluate`

```python
evaluate(simulated, objective="mll", full=False) -> dict
```

| Parameter | Description |
| --- | --- |
| `simulated` | `(n_conditions, n_sim, n_modalities, n_dimensions)`, ordered like `conditions`. |
| `objective` | Objective name. |
| `full` | Also return the predicted and observed distributions, used for plotting and export. |

**Returns**

| Key | Description |
| --- | --- |
| `error` | Scalar to be minimised. |
| `log_likelihood` | Log likelihood, or `NaN` off the likelihood scale. |
| `n_observations` | Number of scored responses. |
| `model_prop`, `data_prop`, `data_counts`, `grids` | Only with `full=True`. One entry per dimension; arrays of shape `(n_conditions, n_modalities, n_grid)`, with `None` for dimensions that have no response model. |
| `r2` | Only with `full=True`. Explained variance between predicted and observed distributions. |

---

## `information_criteria`

```python
information_criteria(log_likelihood, n_free, n_observations) -> dict
```

Returns `{"log_likelihood", "aic", "bic"}` with

```
AIC = 2k − 2·logL
BIC = k·ln(n) − 2·logL
```

where `k = n_free` and `n = n_observations`. A non-finite log likelihood
propagates as `NaN` to both criteria.
