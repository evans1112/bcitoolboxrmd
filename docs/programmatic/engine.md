# `bcitoolbox.engine` — the numerical core

The engine is deliberately free of user-facing objects: it takes plain arrays
and returns plain arrays, so it can be unit tested, reused by the GUI, and
called directly by anyone building something of their own.

---

## `simulate_conditions`

```python
simulate_conditions(conditions, p_common, sigma, mu_prior, sigma_prior,
                    bias=None, strategy="averaging", p_cutoff=0.5,
                    n_sim=10000, seed=13, rng=None,
                    return_internals=False) -> dict
```

Simulate the observer's perceptual estimates for a set of conditions.

| Parameter | Shape / type | Description |
| --- | --- | --- |
| `conditions` | `(n_conditions, n_modalities, n_dimensions)` | Stimulus values. `NaN` marks a modality absent on that dimension: it is dropped from the causal inference and receives no estimate. |
| `p_common` | `float` | Prior probability of a common cause. |
| `sigma` | `(n_modalities, n_dimensions)` | Sensory noise. Strictly positive. |
| `mu_prior`, `sigma_prior` | `(n_dimensions,)` | Prior mean and width per dimension. |
| `bias` | `(n_modalities, n_dimensions)`, optional | Constant added to each measurement. |
| `strategy` | `str` | `"averaging"`, `"selection"` or `"matching"`. |
| `p_cutoff` | `float` | Threshold used by `"selection"`. |
| `n_sim` | `int` | Simulated trials per condition. |
| `seed` | `int` | Seed for the noise. |
| `rng` | `Generator`, optional | Explicit generator; overrides `seed`. |
| `return_internals` | `bool` | Also return measurements and the two per-structure estimates. |

**Returns** a dict with

| Key | Shape | Description |
| --- | --- | --- |
| `estimates` | `(n_conditions, n_sim, n_modalities, n_dimensions)` | Perceptual estimates; `NaN` where a modality was absent. |
| `p_common_posterior` | `(n_conditions, n_sim)` | `p(C = 1 \| x)` on every simulated trial. |
| `conditions`, `strategy`, `n_sim` | | Echoed inputs. |
| `measurements`, `estimate_common`, `estimate_independent` | | Only with `return_internals=True`. |

> **Common random numbers.** The full noise block is drawn up front,
> independently of which cells are present, so the random draws are identical
> across parameter values. Calling the engine twice with the same `seed` gives
> bit-identical output, which is what makes a simulation-based objective
> deterministic and optimisable.

```python
>>> out = btb.simulate_conditions(np.array([[[-10.0], [10.0]]]),
...                               0.5, [[2.0], [8.0]], [0.0], [15.0], n_sim=5000)
>>> out["estimates"].shape
(1, 5000, 2, 1)
```

---

## `log_evidence`

```python
log_evidence(x, sigma, mu_prior, sigma_prior) -> (log_c1, log_c2)
```

Log evidence of both causal structures for one stimulus dimension.

| Parameter | Shape | Description |
| --- | --- | --- |
| `x` | `(n_samples, k)` | Measurements of the `k` modalities present on this dimension. |
| `sigma` | `(k,)` | Their sensory noise. |
| `mu_prior`, `sigma_prior` | `float` | Prior on the source. |

**Returns** `log p(x \| C=1)` and `log p(x \| C=2)`, each `(n_samples,)`.

Works for any `k ≥ 1`. With `k = 1` the two values are **equal**, which is the
mathematically correct statement that a single signal carries no information
about the number of causes — so unimodal trials need no special-casing anywhere
in the toolbox.

---

## `causal_posterior`

```python
causal_posterior(log_c1, log_c2, p_common) -> ndarray
```

Posterior probability of a common cause, computed through a numerically stable
logistic of the log evidence ratio. `p_common = 0` and `p_common = 1` return
exactly `0` and `1`.

---

## `normalise_strategy`

```python
normalise_strategy(strategy) -> str
```

Map any accepted spelling to `"averaging"`, `"selection"` or `"matching"`.
Aliases include `"ave"`, `"sel"`, `"mat"`, `"model averaging"`,
`"probability matching"`. Raises `ValueError` otherwise.
