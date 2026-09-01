# `bcitoolbox.parameters` — free, fixed, bounded and tied parameters

Every quantity in a model is a `Parameter`, and a `Model` owns a `ParameterSet`.
You rarely construct these yourself — `Model.set_param`, `Model.fix` and
`Model.free` delegate to them — but the objects are public, so a parameter set
can be inspected, copied and exported.

---

## `Parameter`

```python
Parameter(name, value=0.0, free=False, bounds=(-inf, inf), init=None,
          tied_to=None, description="")
```

| Attribute | Type | Description |
| --- | --- | --- |
| `name` | `str` | Unique identifier, e.g. `"sigma_visual"`. |
| `value` | `float` | Current value. For a fixed parameter this is the constant used by the model; for a free one it is updated after a fit. |
| `free` | `bool` | `True` if estimated from data. |
| `bounds` | `(float, float)` | Optimisation limits. Ignored while fixed. |
| `init` | `float` or `None` | Optimiser starting value; defaults to `value`. |
| `tied_to` | `str` or `None` | Name of a parameter whose value this one copies. |
| `description` | `str` | Shown in `ParameterSet.summary()`. |

| Property / method | Description |
| --- | --- |
| `start` | Starting value handed to the optimiser, clipped into bounds. |
| `is_estimated` | `True` when the parameter is free **and** not tied. |
| `clip(value)` | Clip a value into the bounds. |
| `copy()` | Independent copy. |

**Raises** `ValueError` if the lower bound exceeds the upper bound, or if a
parameter is both free and tied.

---

## `ParameterSet`

An ordered, name-addressed collection.

### Views

| Property | Description |
| --- | --- |
| `names` | All parameter names, in definition order. |
| `estimated_names` | Names actually optimised (free and not tied). |
| `fixed_names` | Names held constant, including tied ones. |
| `n_free` | Number of estimated parameters — the `k` in AIC and BIC. |

### Editing

| Method | Description |
| --- | --- |
| `set(name, value=None, free=None, bounds=None, init=None, tie=None, description=None)` | Update one parameter; only the arguments you pass are changed. `tie=False` removes an existing tie. |
| `fix(name, value=None)` | Hold constant. |
| `release(name, bounds=None, init=None)` | Estimate. |
| `tie(name, target)` | Force `name` to equal `target`. |
| `add(parameter, overwrite=False)` | Add a new parameter. |

Circular ties (`a → b → a`) raise `ValueError`.

### Value plumbing

These are what connects a named model to a numerical optimiser.

| Method | Returns | Description |
| --- | --- | --- |
| `resolve(values=None)` | `dict` | Complete `{name: value}` mapping with `values` applied as overrides and all ties resolved. |
| `vector()` | `ndarray` | Starting values of the estimated parameters, in order. |
| `bounds()` | `list[tuple]` | Bounds of the estimated parameters, in order. |
| `from_vector(vector)` | `dict` | Turn an optimiser vector into a complete value mapping. |
| `update(values)` | `self` | Write values into the stored parameters (used after a fit). |

### Reporting

| Method | Description |
| --- | --- |
| `to_frame()` | `pandas.DataFrame` with name, value, status, init and bounds. |
| `summary()` | Aligned text table. |
| `copy()` | Deep copy. |

### Example

```python
>>> print(model.params.summary())
parameter                          value  status             lower     upper
----------------------------------------------------------------------------
p_common                             0.5  free                   0         1
mu_prior                               0  free                -100       100
sigma_prior                           10  free                0.01      1000
sigma_visual                           1  free                0.01       100
bias_visual                            0  fixed                  -         -
sigma_motor_visual                     0  fixed                  -         -
sigma_auditory                         1  free                0.01       100
bias_auditory                          0  fixed                  -         -
sigma_motor_auditory                   0  fixed                  -         -
lapse                                  0  fixed                  -         -
p_cutoff                             0.5  fixed                  -         -
----------------------------------------------------------------------------
11 parameters, 5 free
```
