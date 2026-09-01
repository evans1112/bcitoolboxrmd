# BCI Toolbox — Programmatic API

Version 0.3.0

```{toctree}
:hidden:
:maxdepth: 1

quickstart
data
model
parameters
responses
results
plotting
recovery
engine
likelihood
optimizers
theory
```

The BCI Toolbox implements the hierarchical **Bayesian causal inference (BCI)**
model of multisensory perception. Alongside the graphical interface it now ships
a scriptable API designed for reproducible analysis pipelines: build a model
step by step, fit it, simulate it, and export everything.

```python
import bcitoolbox as btb

data  = btb.read_data("sub01.csv",
                      stimulus={"visual": "loc_v", "auditory": "loc_a"},
                      response={"visual": "resp_v", "auditory": "resp_a"})

model = btb.Model.from_data(data)          # architecture inferred from the data
model.set_strategy("averaging")            # decision rule
model.fix("bias_visual", 0.0)              # any parameter can be fixed or freed

fit = model.fit(data)                      # estimate
print(fit.summary())

sim = model.simulate([(-10, 10), (0, 0)],  # explore the fitted model
                     values=fit.values, n=5000)
```

---

## Contents

| Page | Contents |
| --- | --- |
| **[`../examples/tutorial.ipynb`](../examples/tutorial.ipynb)** | **Start here** — a runnable notebook touring every feature in 16 parts |
| [`quickstart.md`](quickstart.md) | Five worked examples: localisation, numerosity, SIFI, two dimensions, parameter recovery |
| [`data.md`](data.md) | `Data`, `read_data` — loading any file layout |
| [`model.md`](model.md) | `Model` — building, fitting, simulating |
| [`parameters.md`](parameters.md) | `Parameter`, `ParameterSet` — free / fixed / bounded / tied |
| [`responses.md`](responses.md) | `ContinuousResponse`, `DiscreteResponse` — task-specific observation models |
| [`results.md`](results.md) | `Fit`, `FitGroup`, `Simulation`, `compare`, `load_fit` |
| [`plotting.md`](plotting.md) | `bcitoolbox.plot` — every figure, all `ax=`-friendly |
| [`recovery.md`](recovery.md) | `recover`, `posterior_predictive`, `Fit.diagnostics` — is this fit trustworthy? |
| [`engine.md`](engine.md) | `simulate_conditions`, `log_evidence` — the numerical core |
| [`likelihood.md`](likelihood.md) | `ScoringPlan`, objectives, information criteria |
| [`optimizers.md`](optimizers.md) | `optimize` — Powell, Nelder–Mead, differential evolution, VBMC |
| [`theory.md`](theory.md) | The model equations, as implemented |

---

## Installation

```bash
pip install bcitoolbox
```

Required: `numpy`, `scipy`, `pandas`.
Optional: `matplotlib` (plotting, `bcitoolbox.plot`), `pyvbmc` (`optimizer="vbmc"`),
`scikit-learn` and `tkinter` (graphical interface).

Importing the package is cheap — the graphical interface, matplotlib and the
legacy functions load only when first used.

### The tutorial notebook

```python
import bcitoolbox as btb
btb.copy_tutorial(".")      # copy it somewhere you can run and edit it
btb.tutorial_path()         # or just find it
```

It runs end to end on packaged and simulated data — no files of your own
needed — and takes a couple of minutes.

#### Open the tutorial step by step

Create a clean analysis folder and virtual environment first:

```bash
mkdir my-bci-analysis
cd my-bci-analysis

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows PowerShell (use these two lines instead)
# py -m venv .venv
# .venv\Scripts\Activate.ps1
```

Install the toolbox and JupyterLab, copy the editable notebook out of the
installed package, and open it:

```bash
python -m pip install "bcitoolbox==0.3.0" jupyterlab
python -c "import bcitoolbox as btb; print(btb.copy_tutorial('.'))"
python -m jupyterlab bcitoolbox_tutorial.ipynb
```

JupyterLab opens in the browser with `bcitoolbox_tutorial.ipynb`. If it asks
for a kernel, select the Python interpreter from `.venv`, then choose
**Run → Run All Cells**. The notebook contains its own packaged and simulated
data, so no data file is required for the first run.

If `bcitoolbox_tutorial.ipynb` already exists, open that copy directly. To
replace it with a fresh copy from the installed package, first rename or remove
the old file, or call `btb.copy_tutorial(".", overwrite=True)` after saving any
work you want to keep.

### Verifying the installation

```bash
python -m bcitoolbox.selftest
```

Runs 28 checks in about ten seconds: the numerical core against the classic
implementation, the documented behaviour of every public object, and parameter
recovery from simulated data. Also available as `btb.selftest()`.

---

## Which paradigm is which

The same machinery covers the paradigms the BCI model is used for; what changes
is the **architecture** you declare and the **response model** you choose.

| Paradigm | Modalities | Dimensions | Response | Reference |
| --- | --- | --- | --- | --- |
| Spatial localisation, ventriloquism | visual, auditory | `space` | `continuous` | Körding et al. 2007; Wozny & Shams 2011 |
| Temporal numerosity, sound-induced flash | visual, auditory | `numerosity` | `discrete` | Shams et al. 2005; Wozny et al. 2008 |
| Visuo-proprioceptive reaching | vision, proprioception | `position` | `continuous` | Körding & Wolpert 2004 |
| Size–weight illusion | size, weight | `heaviness` | `continuous` | Peters et al. 2016 |
| Rubber-hand illusion (ownership) | visual, tactile | `time` + `ownership` | `unity` | Chancel et al. 2022; Chancel & Ehrsson 2023 |
| Unity / common-source judgement | any two | `space` + `unity` | `continuous` + `unity` | Wozny et al. 2010; Acerbi et al. 2018 |
| Numerosity × timing (2-D) | visual, auditory | `numerosity`, `time` | `discrete` | two-dimensional designs |
| Trimodal integration | visual, auditory, tactile | any | any | any number of modalities is supported |

Response scales are irrelevant to the model: the parameter defaults are derived
from your data, so degrees, milliseconds, pixels, counts and 0–1 ratings all
behave the same way.

---

## Design principles

**1. Three objects, in order.** `Data` → `Model` → `Fit`. Every function takes
at most a handful of arguments; anything more detailed is set with a named
method call on the object.

**2. Everything is addressed by name.** There is no parameter ordering to
remember. `model.fix("sigma_auditory", 0.9)` is unambiguous, and the parameter
names are generated from the architecture you declared.

**3. The architecture is declarative.** The number of modalities and stimulus
dimensions is data, not code. Two modalities and one dimension is the classic
case; three modalities, or two dimensions (numerosity × time), work through the
same code path.

**4. Nothing is silently dropped.** If a modality was presented but never
reported — as in the sound-induced flash illusion — the toolbox warns you,
names the affected parameters, and fits anyway.

**5. The response model is the point of extension.** A new paradigm means one
new response model — continuous, discrete, or a judgement about the causal
structure itself — not a new copy of the simulation code.

**6. Simulation is a first-class citizen.** The same model object that fits data
can generate it. `Simulation.to_data()` turns simulated behaviour into a `Data`
object, which is all you need for parameter recovery and power analysis.

---

## Relationship to the graphical interface

The GUI (`btb.gui()`, `btb.gui2d()`) and the legacy functions
(`btb.simulateVV`, `btb.fit`, `btb.fit_2d_bci`, …) are unchanged and fully
supported. The programmatic API is a separate, additional layer.

The numerical core was re-derived in log space and validated against the legacy
implementation to machine precision (see [`theory.md`](theory.md#7-validation)),
so results are directly comparable. Three differences are deliberate
improvements, documented where they occur:

| Topic | Legacy behaviour | Programmatic API |
| --- | --- | --- |
| Absent modality | approximated by a very large sensory noise (σ = 1000) | dropped from the inference exactly |
| Kernel bandwidth (continuous fits) | from the spread pooled **across** conditions | from the spread **within** conditions, per modality — removes a downward bias in the estimated sensory noise |
| Response counts (discrete fits) | reconstructed as `n_trials // (N² − 1)` | the actual observed counts |

---

## Citing

Zhu, H., Beierholm, U., & Shams, L. (2024). BCI Toolbox: An open-source Python
package for the Bayesian causal inference model. *PLOS Computational Biology*,
20(7), e1011791. <https://doi.org/10.1371/journal.pcbi.1011791>
