# `bcitoolbox.model` — building and fitting a model

`Model` is the object you interact with most. It is built in three declarative
steps and used in two.

```python
model = btb.Model(["visual", "auditory"], ["space"])   # 1. architecture
model.set_response("continuous")                       # 2. task
model.set_param("sigma_visual", init=2, bounds=(0.1, 30))
model.fix("bias_visual", 0.0)                          # 3. parameters

fit = model.fit(data)                                  # 4. estimate
sim = model.simulate([(-10, 10), (0, 0)])              # 5. explore
```

Every configuration method returns the model itself, so calls can be chained:

```python
model = (btb.Model(["visual", "auditory"], ["space"])
         .set_response("continuous")
         .set_strategy("all")
         .set_prior(mu=0.0, sigma=(15.0, 1.0, 60.0)))
```

---

## Parameter names

Names are generated from the architecture you declared, so nothing has to be
remembered in a fixed order.

| Name | Meaning | Default |
| --- | --- | --- |
| `p_common` | Prior probability that the signals share a cause | free, `(0, 1)` |
| `sigma_<modality>` | Sensory noise of one modality | free |
| `mu_prior` | Mean of the prior over the source | free |
| `sigma_prior` | Standard deviation of that prior | free |
| `bias_<modality>` | Constant added to a modality's measurement | fixed at 0 |
| `sigma_motor_<modality>` | Response (motor) noise added after the estimate | fixed at 0 |
| `lapse` | Probability of a random response | fixed at 0 |
| `p_cutoff` | Threshold used by the `selection` strategy | fixed at 0.5 |

With more than one stimulus dimension the dimension name is appended:
`sigma_visual_time`, `mu_prior_numerosity`, `bias_auditory_space`.

A dimension whose response model is a
[`UnityResponse`](responses.md#unityresponse) adds `unity_criterion` and has its
own sensory, prior and bias parameters fixed automatically — a judgement about
the causal structure has no stimulus value, so those parameters are meaningless
there.

The five free defaults — `p_common`, the two sensory noises, and the two prior
parameters — match the classic GUI defaults.

---

## Constructor

```python
Model(modalities=("visual", "auditory"), dimensions=("value",),
      response="auto", strategy="averaging", name="")
```

| Parameter | Type | Description |
| --- | --- | --- |
| `modalities` | `list[str]` | Sensory channels. **Any number** is supported; three-modality models work through the same code path. |
| `dimensions` | `list[str]` | Stimulus dimensions, e.g. `["space"]` or `["numerosity", "time"]`. |
| `response` | `str`, `ResponseModel` or `dict` | Response model, applied to every dimension unless a dict `{dimension: response}` is given. `"auto"` defers until data are seen. |
| `strategy` | `str` or `list[str]` | `"averaging"`, `"selection"`, `"matching"`, `"all"`, or a list. A list means "fit each and keep the best". |
| `name` | `str` | Label used in printouts. |

### Several dimensions

Dimensions are independent channels of evidence. Each has its own sensory noise
per modality and its own prior; the evidence for a common cause **multiplies**
across them, so a large temporal offset can prevent integration even when the
spatial disparity is small. Fitting, simulation and `Model.from_data` all work
unchanged; a dimension with no recorded response still informs the causal
inference but contributes nothing to the likelihood.

Visualise a two-dimensional model with
[`plot.posterior_common_2d`](plotting.md#posterior_common_2d) — the integration
window — and [`plot.joint`](plotting.md#joint).

### `Model.from_data`

```python
Model.from_data(data, strategy="averaging", name="", **kwargs) -> Model
```

Builds a model whose architecture mirrors a `Data` object: modalities,
dimensions and response types are taken from the data, and starting values and
bounds are **scaled to the data** (a localisation experiment in degrees and a
numerosity experiment in counts get sensible, different defaults). Anything can
still be overridden afterwards; a setting you make by hand is never overwritten
by the automatic defaults.

---

## Configuration methods

| Method | Description |
| --- | --- |
| `set_strategy(strategy)` | Decision strategy, or several to compare. |
| `set_response(response, dimension=None, **kwargs)` | Response model for one or all dimensions. `kwargs` go to the constructor, e.g. `levels=[0, 1, 2, 3]`. |
| `set_prior(mu=None, sigma=None, dimension=None)` | Configure the prior. Each argument accepts a **number** (fix at that value), `"free"` (estimate with current bounds), or a **tuple** `(init, low, high)` (estimate with those bounds). |
| `set_param(name, value=None, free=None, bounds=None, init=None, tie=None)` | Configure one parameter. Only the arguments you pass are changed. |
| `fix(name, value=None)` | Hold a parameter constant, optionally at a new value. |
| `free(name, bounds=None, init=None)` | Estimate a parameter. |
| `tie(name, target)` | Force one parameter to equal another, e.g. equal noise across modalities. |
| `add_lapse(init=0.02, bounds=(0, 0.5))` | Estimate a lapse rate. |
| `add_motor_noise(init=1.0, bounds=(0, 50), modality=None)` | Estimate response noise. |
| `add_bias(bounds=None, modality=None)` | Estimate a constant sensory bias. |
| `summary()` / `print_summary()` | Human-readable description, including the full parameter table. |
| `copy()` | Deep copy. |
| `to_dict()` / `Model.from_dict(record)` | JSON round-trip of the whole specification. |

### Examples

```python
model.fix("p_common", 0.5)                       # fix at a value
model.free("bias_visual", bounds=(-10, 10))      # estimate with bounds
model.set_param("sigma_visual", init=2.0, bounds=(0.1, 30))
model.tie("sigma_auditory", "sigma_visual")      # equal-noise model
model.set_prior(mu=0.0, sigma="free")            # fixed mean, free width
```

---

## `Model.fit`

```python
fit(data, objective="mll", optimizer="powell", n_sim=10000, n_start=1,
    strategy=None, by=None, seed=13, progress=None, options=None) -> Fit | FitGroup
```

| Parameter | Type | Description |
| --- | --- | --- |
| `data` | `Data` | Behavioural data. Its modalities and dimensions must match the model. |
| `objective` | `str` | `"mll"` (default), `"sse"`, `"r2"` or `"emd"` — see [`likelihood.md`](likelihood.md). |
| `optimizer` | `str` | `"powell"` (default), `"neldermead"`, `"lbfgs"`, `"differential_evolution"` or `"vbmc"` — see [`optimizers.md`](optimizers.md). |
| `n_sim` | `int` | Simulated trials per condition. 1000 while exploring, 10000 for results you intend to report. |
| `n_start` | `int` | Starting points for the optimiser. Values above 1 also give a convergence diagnostic. |
| `strategy` | `str` or `list[str]`, optional | Overrides the model's strategy for this fit. Several strategies are fitted separately and the best is returned; all are kept in `fit.strategy_comparison`. |
| `by` | `str`, optional | Fit each group separately, usually `"subject"`. Returns a `FitGroup`. |
| `seed` | `int` | Seed for the simulation noise. Held fixed across optimiser iterations (**common random numbers**), which makes the objective deterministic and much easier to optimise. |
| `progress` | `callable`, optional | `progress(message)` called with short status strings. |
| `options` | `dict`, optional | Extra options forwarded to the optimiser. |

**Returns:** `Fit`, or `FitGroup` when `by` is given.

**Warns** (`UserWarning`) when a modality is presented but never reported, or
never presented at all, while its parameters are still free. The message names
the affected parameters and the exact call that fixes them. **Fitting
continues** — the warning is advice, not an error.

```
UserWarning: No responses were recorded for modality 'auditory' in 'sifi'. Its
parameters (sigma_auditory) are only weakly constrained, through the other
modality's responses. Fitting will continue, but you should normally fix them at
a value from an independent measurement, e.g. model.fix('sigma_auditory', <value>).
```

---

## `Model.simulate`

```python
simulate(conditions, values=None, n=10000, strategy=None, seed=13,
         apply_response=True) -> Simulation
```

Generate behaviour from the model, with or without any data.

| Parameter | Type | Description |
| --- | --- | --- |
| `conditions` | `Data`, array or list of tuples | The conditions to simulate. A `Data` object contributes its unique conditions; a list of tuples such as `[(-10, 10), (0, 0)]` works for single-dimension models; otherwise pass an array of shape `(n_conditions, n_modalities, n_dimensions)`. `NaN` marks an absent modality. |
| `values` | `dict`, optional | Parameter values overriding the model's current ones, e.g. `values=fit.values`. |
| `n` | `int` | Simulated trials per condition. |
| `strategy` | `str`, optional | Decision strategy for this simulation. |
| `seed` | `int` | Random seed. |
| `apply_response` | `bool` | Apply motor noise, lapses and discretisation. `False` returns the raw perceptual estimates. |

**Returns:** [`Simulation`](results.md#simulation)

```python
# What does this observer do when the two signals disagree by 20 degrees?
sim = model.simulate([(-10, 10)], values={"p_common": 0.7}, n=20000)
sim.summary()          # per-condition means, SDs, and mean p(C=1)
sim.to_frame()         # one row per simulated trial
sim.to_data()          # -> Data, ready to be fitted (parameter recovery)
```

---

## `Model.predict`

```python
predict(data, values=None, n_sim=None, strategy=None, seed=13) -> dict
```

Predicted and observed response distributions for a data set, in the format
used for plotting and for exporting predictions. Returns `model_prop`,
`data_prop`, `data_counts` and `grids` (one entry per dimension), plus
`conditions`, `error`, `log_likelihood` and `r2`.

---

## Other methods

| Method | Description |
| --- | --- |
| `values(overrides=None)` | Complete `{name: value}` mapping with ties applied. |
| `conditions_array(conditions)` | Normalise a user-supplied condition specification to `(n_conditions, n_modalities, n_dimensions)`. |
| `params` | The underlying [`ParameterSet`](parameters.md). |
