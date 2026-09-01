# `bcitoolbox.plot` — visualisation

Every plotting function follows the same contract:

* it takes **one object** (`Data`, `Model`, `Fit`, `FitGroup` or `Simulation`)
  plus a few options;
* it accepts `ax=` so the plot can be dropped into a figure you already have;
* it **returns** the `Axes` — or the `Figure` when it had to create a grid of
  panels — so you can keep customising it;
* it never calls `show()` or `savefig()`; that stays your decision.

```python
import bcitoolbox as btb
import matplotlib.pyplot as plt

btb.plot.set_style("notebook")
btb.plot.fit(fit)
plt.show()
```

Matplotlib is imported the first time `btb.plot` is touched, so scripts that
never plot stay light.

---

## Overview

| Function | Shows |
| --- | --- |
| [`data`](#data) | Observed response distributions, one panel per condition |
| [`fit`](#fit) | Model predictions against the data, one panel per condition |
| [`simulation`](#simulation) | Simulated response distributions |
| [`bias`](#bias) | Crossmodal bias — the ventriloquism curve |
| [`posterior_common`](#posterior_common) | `p(C = 1)` as a function of disparity |
| [`posterior_common_2d`](#posterior_common_2d) | `p(C = 1)` over **two** dimensions — the integration window |
| [`joint`](#joint) | Joint response distribution across two dimensions |
| [`posterior_predictive`](#posterior_predictive) | Observed statistics against their predictive intervals |
| [`params`](#params) | Parameter estimates, for one fit or across subjects |
| [`model_comparison`](#model_comparison) | ΔAIC / ΔBIC across models or strategies |
| [`recovery`](#recovery) | True against estimated parameters |
| [`rdm`](#rdm) | Representational dissimilarity matrix |
| [`landscape`](#landscape) | Objective landscape over one or two parameters |

Accessors are attached to the objects themselves, so `fit.plot.fit()` and
`btb.plot.fit(fit)` are the same call:

| Object | Available as |
| --- | --- |
| `Fit` | `.plot.fit()`, `.plot.data()`, `.plot.bias()`, `.plot.params()`, `.plot.posterior_common()`, `.plot.posterior_common_2d()`, `.plot.joint()`, `.plot.posterior_predictive()`, `.plot.rdm()`, `.plot.model_comparison()` |
| `FitGroup` | `.plot.params()` |
| `Simulation` | `.plot.distributions()`, `.plot.joint()` |
| `Data` | `.plot.distributions()`, `.plot.bias()` |

---

## `set_style`

```python
set_style(context="paper", grid=False) -> dict
```

Apply a clean, publication-oriented matplotlib style. `context` is `"paper"`,
`"notebook"` or `"talk"` and scales fonts and line widths. Returns the rcParams
it applied.

`PALETTE` holds the default modality colours, and
`modality_colors(modalities)` maps names to colours so that a modality keeps the
same colour across every figure. Pass `colors={"visual": "#000000"}` to any
function to override.

---

## `data`

```python
data(dataset, dimension=None, conditions=None, max_conditions=36,
     bins=15, ax=None, colors=None)
```

Observed response distributions, one panel per condition. Bimodal conditions are
drawn first. Discrete responses become grouped bars, continuous responses become
histograms; a dotted vertical line marks each modality's stimulus.

---

## `fit`

```python
fit(fit_object, dimension=None, conditions=None, max_conditions=36,
    n_sim=None, ax=None, colors=None)
```

Model predictions against observed data — the modern replacement for the classic
`plotKonrads` figure. Data are filled, the model is dashed, and the title carries
the data name, the winning strategy and the distribution `r²`.

Predictions stored by the fit are reused; pass `n_sim=` to recompute them with a
different number of simulated trials (worth doing for a final figure).

---

## `simulation`

```python
simulation(sim, dimension=None, conditions=None, max_conditions=36,
           bins=25, ax=None, colors=None, show_p_common=True)
```

Simulated response distributions, one panel per condition, each annotated with
the mean posterior probability of a common cause.

---

## `bias`

```python
bias(source, dimension=None, relative=True, n_sim=None, ax=None, colors=None)
```

Crossmodal bias. `source` may be a `Fit` (data as markers, model as lines) or a
bare `Data`.

**`relative=True`** (default) — the classic ventriloquism curve. The x axis is
the signed disparity between the two stimuli; the y axis is the mean response
*relative to that modality's own stimulus*. A flat line at zero means no
integration; a line along the diagonal means complete capture by the other
modality. Averaging over the modality's own positions is legitimate here
precisely because the plotted quantity is relative to that position.

The signature of causal inference is visible in this plot: the bias of the
unreliable modality first grows with disparity and then **saturates and falls
back**, because the observer starts to infer separate causes. Forced fusion
predicts a straight line instead.

**`relative=False`** — the raw mean response against the modality's own stimulus,
one line per level of the other modality, one panel per modality.

Raises `ValueError` if the design has no bimodal conditions, or if
`relative=True` is used with more than two modalities, where "the other stimulus"
is undefined.

---

## `posterior_common`

```python
posterior_common(model, values=None, disparities=None, centre=None, n=4000,
                 dimension=None, strategy=None, ax=None, label=None)
```

Mean posterior probability of a common cause as a function of disparity. Needs a
two-modality model. Overlay several parameter sets by calling it repeatedly with
the same `ax` and different `label`:

```python
ax = btb.plot.posterior_common(model, values={"p_common": 0.2}, label="p=0.2")
btb.plot.posterior_common(model, values={"p_common": 0.8}, label="p=0.8", ax=ax)
```

---

## `posterior_common_2d`

```python
posterior_common_2d(model, values=None, dimensions=None, disparities=None,
                    n=1500, strategy=None, ax=None, cmap="magma", levels=9)
```

`p(C = 1)` as a function of the disparity on **each of two dimensions** — the
integration window of a two-dimensional model, with the `p = 0.5` contour drawn
in white.

The shape is the interesting part. Concentric contours mean the two dimensions
contribute independently; an elongated map means one dimension dominates, which
happens when its sensory noise is small relative to its prior.

```python
btb.plot.posterior_common_2d(fit.model, values=fit.values)
```

---

## `joint`

```python
joint(source, dimensions=None, conditions=None, max_conditions=9, n_sim=None,
      ax=None, colors=None, levels=6)
```

The joint response distribution across two dimensions, one panel per condition.
Each modality is drawn as density contours in the plane spanned by the two
dimensions, with its stimulus marked by a cross; when a `Fit` is passed, the
observed responses are overlaid as points.

This is where two-dimensional causal inference becomes visible: at zero
disparity on both dimensions the two clouds collapse together, at large
disparity on both they sit on their own stimuli, and at large disparity on only
one they stretch into the characteristic partially-integrated shape.

Raises `ValueError` if fewer than two dimensions carry responses.

---

## `posterior_predictive`

```python
posterior_predictive(check, ax=None, color=None)
```

Observed statistics against their posterior predictive intervals — one point
per (condition, modality) cell, the 95% interval as a vertical bar, cells
outside the interval highlighted. Takes the object returned by
`btb.posterior_predictive(fit)`; see [`recovery.md`](recovery.md).

---

## `params`

```python
params(source, names=None, ax=None, show_bounds=True, color=None)
```

For a `Fit`: a dot plot of each estimate with its optimisation bounds behind it —
an estimate sitting on its bound is immediately visible, which usually means the
bound is too tight.

For a `FitGroup`: the distribution across fits, with the group mean and its 95%
interval.

---

## `model_comparison`

```python
model_comparison(fits, criterion="bic", ax=None, color=None)
```

Bar chart of ΔBIC (or ΔAIC), best model at zero. `fits` may be a list, a
`{label: fit}` dict, or a single `Fit` that was fitted with `strategy="all"`, in
which case its strategies are compared.

Raises `ValueError` if the criterion is undefined — only likelihood objectives
(`objective="mll"`) define AIC and BIC.

---

## `recovery`

```python
recovery(pairs, names=None, ncols=3, figsize=None, color=None)
```

True against estimated parameters, one panel per parameter, with the identity
line and the `r²`. `pairs` is either a list of `(true_values, fit)` tuples — the
natural output of a recovery loop — or a frame with columns `parameter`, `true`
and `estimated`.

```python
pairs = []
for seed in range(20):
    truth = {"p_common": rng.uniform(0.1, 0.9),
             "sigma_visual": rng.uniform(1, 5),
             "sigma_auditory": rng.uniform(4, 14)}
    generated = generator.simulate(conditions, values=truth, n=60,
                                   seed=seed).to_data()
    pairs.append((truth, btb.Model.from_data(generated).fit(generated)))

btb.plot.recovery(pairs)
```

---

## `rdm`

```python
rdm(source, dimension=None, n_sim=None, ax=None, cmap="BuGn", labels=False)
```

Representational dissimilarity matrix: each condition is described by its
predicted response distribution stacked across modalities, and the matrix holds
the Euclidean distance between every pair of conditions. Intended for comparison
with neuroimaging RDMs.

> Advanced feature. The distances depend on how the response distributions are
> discretised, so only compare RDMs between models fitted with the same response
> grid.

---

## `landscape`

```python
landscape(model, dataset, x, y=None, values=None, n_grid=15, n_sim=1000,
          objective="mll", strategy=None, ax=None, cmap="viridis")
```

Objective landscape over one parameter (a profile) or two (a heat map), with the
current values marked. This is the fastest way to see whether an optimum is a
real minimum or a flat ridge, and to spot parameters that trade off against each
other — `mu_prior` and `sigma_prior` often do.

Cost is `n_grid` or `n_grid²` simulations, so keep both `n_grid` and `n_sim`
modest while exploring.

```python
btb.plot.landscape(fit.model, data, "p_common", values=fit.values,
                   n_grid=11, n_sim=800)
btb.plot.landscape(fit.model, data, "sigma_visual", "sigma_auditory",
                   values=fit.values, n_grid=9, n_sim=500)
```
