# `bcitoolbox.optimizers` — searching the parameter space

All optimisers share one interface, so switching between a fast local search and
a global or Bayesian method is a one-word change.

| `optimizer=` | Method | When to use it |
| --- | --- | --- |
| `"powell"` | Bounded Powell (SciPy) | **Default.** Derivative-free and robust to the mild stochasticity of a simulation-based objective. |
| `"neldermead"` | Bounded Nelder–Mead (SciPy) | Alternative simplex search. |
| `"lbfgs"` | L-BFGS-B (SciPy) | Only for smooth objectives; it will struggle with a noisy one. |
| `"differential_evolution"` (`"de"`) | Global search (SciPy) | Slow but insensitive to the starting point. A good cross-check when a fit looks suspicious. |
| `"vbmc"` | Variational Bayesian Monte Carlo (`pyvbmc`) | Returns an approximate **posterior** over the parameters, not just a point estimate. |

---

## `optimize`

```python
optimize(objective, x0, bounds, method="powell", n_start=1, seed=13,
         callback=None, options=None) -> OptimizationResult
```

| Parameter | Type | Description |
| --- | --- | --- |
| `objective` | `callable` | `f(x) -> float` on a 1-D parameter vector. |
| `x0` | `array_like` | Initial vector. |
| `bounds` | `list[(low, high)]` | One pair per parameter. |
| `method` | `str` | Optimiser name or alias. |
| `n_start` | `int` | Starting points. The first is always `x0`; the rest are spread inside the bounds with a fixed seed, so the fit is reproducible. |
| `seed` | `int` | Seed for the extra starting points and for `differential_evolution`. |
| `callback` | `callable`, optional | `callback(info)` after every start, with `start`, `n_starts`, `fun` and `x`. |
| `options` | `dict`, optional | Forwarded to the underlying optimiser. |

**Raises** `ImportError` if `method="vbmc"` and `pyvbmc` is not installed;
`ValueError` if `"differential_evolution"` or `"vbmc"` is given non-finite
bounds.

The objective is wrapped so that `NaN`, `inf` and numerical exceptions are
converted into a large finite penalty — a single bad parameter combination
cannot abort a fit.

---

## `OptimizationResult`

| Attribute | Description |
| --- | --- |
| `x` | Best parameter vector. |
| `fun` | Objective value at `x`. |
| `success`, `message` | Convergence flag and diagnostic text. |
| `method` | Canonical optimiser name. |
| `n_evaluations` | Objective evaluations across all starts. |
| `seconds` | Wall-clock duration. |
| `starts` | One entry per starting point: `{"x0", "x", "fun", "success"}`. |
| `posterior` | Approximate posterior from `vbmc`, otherwise `None`. |
| `extras` | Method-specific extras — for VBMC the ELBO, its SD, the posterior samples and their SD. |
| `converged_consistently` | `True` when every start reached essentially the same objective. **If this is `False`, the objective has local minima: raise `n_start` or narrow the bounds before trusting the fit.** |

---

## Notes on VBMC

`optimizer="vbmc"` returns the posterior **mean** as the point estimate and
keeps the full variational posterior in `fit.optimization.posterior`, with
posterior samples in `fit.optimization.extras["posterior_samples"]`. Model
comparison still uses the objective value at that point estimate, so `error`,
`AIC` and `BIC` remain comparable with fits from the other optimisers.

VBMC is expensive: budget roughly a hundred times the runtime of a Powell fit,
and start from `n_sim = 1000` while you calibrate.
