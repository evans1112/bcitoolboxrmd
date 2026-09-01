# `bcitoolbox.responses` — task-specific observation models

The engine produces *perceptual estimates*. What an experiment records is a
*response*. A response model owns the mapping between them, the support of the
response scale, and the likelihood used to score observed against simulated
responses.

| Task | Response model |
| --- | --- |
| Spatial localisation, matching, pointing, reaching | `ContinuousResponse` |
| Numerosity judgement, rating scale, forced choice | `DiscreteResponse` |
| "Same source?", body-ownership, "simultaneous?" | `UnityResponse` |

Adding a new paradigm means writing one new subclass, not copying the
simulation code.

---

## `make_response_model`

```python
make_response_model(spec, **kwargs) -> ResponseModel
```

Build a response model from a name, a class or an instance. Accepted names:
`"continuous"` (`"cont"`, `"real"`, `"localisation"`, `"localization"`) and
`"discrete"` (`"disc"`, `"count"`, `"numerosity"`). Keyword arguments are
forwarded to the constructor.

```python
btb.make_response_model("discrete", levels=[0, 1, 2, 3])
```

---

## `DiscreteResponse`

```python
DiscreteResponse(levels=None, epsilon=1e-3, name=None)
```

Responses drawn from a small set of levels. Simulated estimates are snapped to
the nearest level, and the likelihood is multinomial over the observed counts.

| Parameter | Type | Description |
| --- | --- | --- |
| `levels` | `array_like`, optional | Allowed responses. Learned from the data when omitted. |
| `epsilon` | `float` | Weight of a uniform mixture added to the model probabilities before taking logarithms, so that a response the model considers impossible does not produce `-inf`. The classic toolbox uses `0.001`. |

| Method | Description |
| --- | --- |
| `apply(estimates, rng, motor_sigma=0.0, lapse=0.0)` | Add motor noise and lapses, then snap to the nearest level. |
| `probabilities(values)` | Probability of each level. |
| `counts(values)` | Number of responses at each level. |
| `grid()` | The levels. |
| `log_likelihood_cell(simulated, observed, modality=None)` | Multinomial log likelihood. |
| `configure(data, dimension_index)` | Learn the levels from data. |

---

## `ContinuousResponse`

```python
ContinuousResponse(bandwidth=None, support=None, n_bins=20,
                   max_kernel_samples=2000, name=None)
```

Real-valued responses. The likelihood is a Gaussian kernel density estimate of
the simulated responses evaluated at the observed ones.

| Parameter | Type | Description |
| --- | --- | --- |
| `bandwidth` | `float`, optional | Fixed kernel bandwidth. Learned from the data when omitted — see the note below. |
| `support` | `(float, float)`, optional | Range used for lapse responses and for binning. Learned from the data when omitted. |
| `n_bins` | `int` | Bins used by the distribution-based objectives (`sse`, `r2`). The likelihood itself is not binned. |
| `max_kernel_samples` | `int` | Cap on the simulated samples entering one kernel density evaluation; keeps the objective fast for large `n_sim`. |

| Method | Description |
| --- | --- |
| `apply(estimates, rng, motor_sigma=0.0, lapse=0.0)` | Add motor noise and lapses. |
| `bandwidth_for(modality=None, n_samples=None)` | The bandwidth actually used for one modality. |
| `probabilities(values)` | Histogram over `grid()`. |
| `grid()` | Bin centres. |
| `log_likelihood_cell(simulated, observed, modality=None)` | Kernel-density log likelihood. |
| `configure(data, dimension_index)` | Learn the bandwidth and support from data. |

> ### How the bandwidth is chosen, and why it matters
>
> A kernel density likelihood adds the kernel's variance to the model's own.
> If the bandwidth `h` is large relative to the true sensory noise `σ`, the
> optimiser compensates by **shrinking `σ`**, and the fitted sensory noise comes
> out too small — an artefact of the estimator, not a property of the observer.
>
> The bandwidth is therefore derived from the spread of the responses **within**
> a condition, separately for each modality, using Silverman's rule with the
> number of *simulated* samples in the rate:
>
> ```
> h = 1.06 · σ_within · n_sim^(−1/5)
> ```
>
> Pooling responses *across* conditions — as the legacy `fre` objective does —
> inflates `σ_within` by the spread of the condition means and produces a badly
> oversized kernel. In a localisation recovery test with a true
> `sigma_visual = 2.0`, the pooled bandwidth returned `0.80` (−60%); the
> within-condition bandwidth returns `1.95` (−2.5%).
>
> Passing an explicit `bandwidth=` always overrides the automatic choice.

---

## Helper functions

```python
robust_scale(values, min_scale=1e-9) -> float
```
Robust spread: the smaller of the standard deviation and IQR/1.349.

```python
silverman_bandwidth(values, n_samples=None, min_bandwidth=1e-6) -> float
```
Silverman's rule of thumb. `n_samples` sets the sample size entering the
`n^(−1/5)` rate; when the density is built from simulated responses this should
be the number of *simulated* samples, not the number of observations.

---

## `UnityResponse`

```python
UnityResponse(rule="criterion", epsilon=1e-3, name=None)
```

A yes/no judgement about the **causal structure itself**. Unlike every other
response model it is driven by the posterior probability of a common cause
rather than by a perceptual estimate, which makes a large family of paradigms
available:

* **unity judgements** — "did the flash and the beep come from the same place?"
  — often collected alongside a localisation response in the same trial;
* **body-ownership reports** in the rubber-hand illusion — "did the rubber hand
  feel like your own?" — as a function of visuotactile asynchrony;
* any "same source / different source" or "simultaneous / not" report.

Responses are coded `1` for a common cause and `0` for separate causes, and the
likelihood is Bernoulli.

| Parameter | Description |
| --- | --- |
| `rule` | `"criterion"` reports a common cause when the posterior exceeds the `unity_criterion` model parameter (0.5 by default, free to estimate). `"matching"` reports a common cause *with probability* equal to the posterior — the explicit analogue of probability matching. |
| `epsilon` | Uniform mixing weight that keeps the likelihood finite. |

### Setting it up

A dimension carrying such a judgement has **no stimulus** — the judgement is
about the causal structure, not about a stimulus value. Build the data with a
response column but no stimulus column for that dimension:

```python
data = btb.read_data("rhi.csv",
                     stimulus={"visual":  {"time": "t_vision"},
                               "tactile": {"time": "t_touch"}},
                     response={"visual":  {"ownership": "felt_like_mine"}},
                     dimensions=["time", "ownership"])
```

`Model.from_data` then recognises the dimension automatically. Doing it by hand
is one call:

```python
model.set_response("unity", dimension="ownership")
```

which also fixes the sensory, prior and bias parameters of that dimension —
they have no meaning there — and adds `unity_criterion`.

> **Watch out for identifiability.** With a *symmetric* yes/no judgement as the
> only response, the two sensory noises enter the model almost entirely through
> their sum, so they cannot be estimated separately. `fit.diagnostics()` detects
> this; tie them or fix one. See [`recovery.md`](recovery.md#fitdiagnostics).

---

## Writing your own

```python
class MyResponse(btb.ResponseModel):
    kind = "my_task"

    def configure(self, data, dimension_index):
        ...          # learn anything task-specific; must not depend on parameters
        return self

    def apply(self, estimates, rng, motor_sigma=0.0, lapse=0.0, **context):
        ...          # estimates -> responses
        # context may carry 'posterior' and 'criterion'; set the class
        # attribute needs_posterior = True to request them
        return responses

    def grid(self):
        ...          # the support used for summaries

    def probabilities(self, values):
        ...          # probability vector over grid()

    def log_likelihood_cell(self, simulated, observed, modality=None):
        ...          # scalar log likelihood
```

Pass an instance straight to `model.set_response(MyResponse())`.
