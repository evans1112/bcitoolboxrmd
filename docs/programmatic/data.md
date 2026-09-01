# `bcitoolbox.data` — behavioural data

A `Data` object stores stimuli and responses in one canonical shape, whatever
the raw file looked like:

```
stimulus : (n_trials, n_modalities, n_dimensions)
response : (n_trials, n_modalities, n_dimensions)
```

Two conventions carry all the "messy experiment" information:

| Convention | Meaning |
| --- | --- |
| `NaN` in `stimulus` | That modality was **not presented** on that trial (a unimodal trial). The model treats the trial as having a single signal; no causal inference is performed. |
| `NaN` in `response` | That response was **not collected**. Whole columns may be `NaN` — only the flash is reported in the SIFI, only the primary dimension is reported in a 2-D design. Those cells are excluded from the likelihood. |

---

## `read_data`

```python
read_data(path, stimulus=None, response=None, dimensions=None, subject=None,
          covariates=None, missing=None, missing_dimension=None,
          layout=None, modalities=None, name=None, **read_kwargs) -> Data
```

Load a `.csv`, `.tsv`, `.txt`, `.xls` or `.xlsx` file.

| Parameter | Type | Description |
| --- | --- | --- |
| `path` | `str` | Path to the file. |
| `stimulus` | `dict` | `{modality: column}` for a one-dimensional experiment, or `{modality: {dimension: column}}` for several dimensions. |
| `response` | `dict` | Same structure. A modality or dimension that was never reported may be omitted entirely. |
| `dimensions` | `list[str]`, optional | Explicit dimension order; inferred from the mapping otherwise. |
| `subject` | `str`, optional | Column holding the subject identifier, for `Model.fit(..., by="subject")`. |
| `covariates` | `list[str]`, optional | Extra columns to keep for grouping and plotting. |
| `missing` | `float`, optional | Value marking an **absent modality** (`missing=0` for legacy numerosity files). See the note below. |
| `missing_dimension` | `str`, optional | Dimension carrying the presence code; defaults to the first dimension. |
| `layout` | `"legacy"`, optional | Read the classic headerless BCI Toolbox file. |
| `modalities` | `list[str]`, optional | Modality names when `layout="legacy"`. |
| `name` | `str`, optional | Label for printouts; defaults to the file name. |
| `**read_kwargs` | | Forwarded to `pandas.read_csv` / `read_excel`. |

**Returns:** `Data`

**Raises:** `KeyError` if a named column is absent; `ValueError` if neither a
mapping nor `layout="legacy"` is given.

> **How `missing` works.** It is looked up on **one** dimension only, and marks
> the whole modality absent on that trial. This matters in multi-dimensional
> designs: `0` flashes means "no visual stimulus", but an SOA of `0 ms` is a
> perfectly good stimulus value. Setting `missing=0` with
> `missing_dimension="numerosity"` marks the modality absent from the flash
> count alone and leaves the SOA untouched.

### Examples

```python
# Standard: named columns
data = btb.read_data("sub01.csv",
                     stimulus={"visual": "loc_v", "auditory": "loc_a"},
                     response={"visual": "resp_v", "auditory": "resp_a"},
                     subject="participant")

# Legacy four-column file (stim_1, stim_2, resp_1, resp_2), no header
data = btb.read_data("demo.csv", layout="legacy",
                     modalities=["visual", "auditory"],
                     dimensions=["numerosity"])

# Only one modality is ever reported (SIFI)
data = btb.read_data("sifi.csv",
                     stimulus={"visual": "flash", "auditory": "beep"},
                     response={"visual": "report_flash"},
                     dimensions=["numerosity"], missing=0)

# Two stimulus dimensions
data = btb.read_data("av2d.csv",
                     stimulus={"visual":   {"numerosity": "F", "time": "tF"},
                               "auditory": {"numerosity": "B", "time": "tB"}},
                     response={"visual":   {"numerosity": "rF"},
                               "auditory": {"numerosity": "rB"}},
                     missing=0, missing_dimension="numerosity")
```

---

## `Data`

```python
Data(stimulus, response, modalities, dimensions, subject=None,
     covariates=None, name="", drop_absent_responses=True)
```

Usually built through `read_data` or the constructors below.

`drop_absent_responses=True` (the default) sets to `NaN` any response belonging
to a modality that was not presented, which removes meaningless placeholder
values such as the `0` used in legacy files.

### Constructors

| Method | Description |
| --- | --- |
| `Data.from_frame(frame, stimulus, response, dimensions=None, subject=None, covariates=None, missing=None, missing_dimension=None, name="")` | Build from a `pandas.DataFrame` using a column mapping. |
| `Data.from_arrays(stimulus, response, modalities=None, dimensions=None, subject=None, covariates=None, name="")` | Build from plain arrays. 2-D input `(n_trials, n_modalities)` is accepted for single-dimension experiments. |

### Attributes

| Attribute | Type | Description |
| --- | --- | --- |
| `stimulus`, `response` | `ndarray` | The canonical 3-D arrays. |
| `modalities`, `dimensions` | `list[str]` | Names. |
| `n_trials`, `n_modalities`, `n_dimensions` | `int` | Shape. |
| `conditions` | `ndarray (n_conditions, n_mod, n_dim)` | Unique stimulus conditions. |
| `condition_index` | `ndarray (n_trials,)` | Condition of every trial. |
| `n_conditions` | `int` | Number of unique conditions. |
| `presented` | `ndarray (n_modalities,) of bool` | Was this modality ever presented? |
| `reported` | `ndarray (n_mod, n_dim) of bool` | Was this cell ever reported? |
| `reported_modalities` | `list[str]` | Modalities with at least one response. |
| `unreported_modalities` | `list[str]` | Presented but never reported — these trigger the fitting warning. |
| `reported_dimensions` | `list[str]` | Dimensions with at least one response. |
| `subject` | `ndarray` or `None` | Per-trial subject identifier. |
| `covariates` | `dict` | Extra per-trial columns. |

### Methods

| Method | Description |
| --- | --- |
| `condition_counts()` | Trials per condition, `ndarray (n_conditions,)`. |
| `response_levels(dimension=None)` | Sorted unique responses on one dimension. |
| `suggest_response_kind(dimension=None)` | `"discrete"` or `"continuous"`, inferred from the responses. |
| `select(mask, name=None)` | New `Data` restricted to the trials in `mask`. |
| `split(by="subject")` | `OrderedDict` of `{group: Data}`; `by` may be `"subject"` or a covariate name. |
| `to_frame()` | Tidy `pandas.DataFrame`, one row per trial. |
| `summary()` | Multi-line description: trials, conditions, coverage per modality, response type per dimension, and any identifiability warning. |

### Example

```python
>>> print(data.summary())
Data: demo
  trials      : 225
  modalities  : visual, auditory
  dimensions  : numerosity
  conditions  : 15
  visual      : presented on 180 trials, reported on 180 trials
  auditory    : presented on 180 trials, reported on 0 trials
  numerosity  : discrete responses, 4 levels [0, 1, 2, 3]

  note: no responses recorded for auditory. Its sensory noise parameter cannot be
        estimated from these data - fix it with model.fix('sigma_<modality>', value).
```
