# Quickstart — five worked examples

Every example is self-contained and runs as written. For a guided tour of the
whole API, run the notebook instead:

```python
import bcitoolbox as btb
btb.copy_tutorial(".")
```

---

## 1. Spatial localisation (continuous responses)

The classic audiovisual localisation paradigm: on each trial a flash and a beep
appear at some spatial disparity, and the participant reports both locations.

```python
import bcitoolbox as btb

data = btb.read_data("sub01.csv",
                     stimulus={"visual": "loc_v", "auditory": "loc_a"},
                     response={"visual": "resp_v", "auditory": "resp_a"})

model = btb.Model.from_data(data)         # continuous responses detected
fit = model.fit(data, n_sim=10000)
print(fit.summary())

fit.values["p_common"]      # 0.62
fit.bic                     # 13302.3
```

Compare the three decision strategies in one call:

```python
fit = model.fit(data, strategy="all")
print(fit.strategy)                 # 'averaging'
print(fit.strategy_comparison)      # error, log likelihood, AIC and BIC for each
```

---

## 2. Numerosity judgement (discrete responses)

Flashes and beeps; the participant reports how many of each they perceived.
Absent modalities are coded as `0` in the classic file format.

```python
data = btb.read_data("numerosity.csv",
                     stimulus={"visual": "n_flash", "auditory": "n_beep"},
                     response={"visual": "r_flash", "auditory": "r_beep"},
                     dimensions=["numerosity"], missing=0)

model = btb.Model.from_data(data)
model.set_response("discrete", levels=[0, 1, 2, 3, 4])
model.set_prior(mu=2.0, sigma=3.0)     # weakly identified here: fix them
fit = model.fit(data, n_sim=10000, n_start=3)

print(fit.summary())
print(fit.optimization.converged_consistently)   # True -> the optimum is stable
```

A classic headerless four-column file loads with one argument:

```python
data = btb.read_data("demo.csv", layout="legacy",
                     modalities=["visual", "auditory"],
                     dimensions=["numerosity"])
```

---

## 3. Sound-induced flash illusion — only one modality is reported

In the SIFI only the number of *flashes* is reported, so the auditory response
column does not exist. The toolbox fits anyway and tells you which parameters
the data cannot constrain.

```python
data = btb.read_data("sifi.csv",
                     stimulus={"visual": "flash", "auditory": "beep"},
                     response={"visual": "report_flash"},   # auditory omitted
                     dimensions=["numerosity"], missing=0)

print(data.unreported_modalities)      # ['auditory']

model = btb.Model.from_data(data)
fit = model.fit(data)
# UserWarning: No responses were recorded for modality 'auditory'. Its
# parameters (sigma_auditory) are only weakly constrained ... you should
# normally fix them, e.g. model.fix('sigma_auditory', <value>).
```

Follow the advice — typically with a value from a unimodal control block or
from the literature — and the warning disappears:

```python
model = btb.Model.from_data(data)
model.fix("sigma_auditory", 0.9)
fit = model.fit(data)                  # 4 free parameters, no warning
```

---

## 3b. Rubber-hand illusion — a yes/no judgement about the causal structure

Participants judge whether the rubber hand felt like their own, at a range of
visuotactile asynchronies. There is no continuous response at all: the report
*is* the causal inference.

```python
data = btb.read_data("rhi.csv",
                     stimulus={"visual":  {"time": "t_vision"},
                               "tactile": {"time": "t_touch"}},
                     response={"visual":  {"ownership": "felt_like_mine"}},
                     dimensions=["time", "ownership"])

model = btb.Model.from_data(data)          # the 'ownership' dimension is
                                           # recognised as a unity judgement
model.set_prior(mu=0.0, sigma=800.0, dimension="time")
model.tie("sigma_tactile_time", "sigma_visual_time")   # see the note below

fit = model.fit(data, n_start=4)
print(fit.diagnostics()["text"])
```

> A symmetric yes/no judgement constrains the two sensory noises almost only
> through their **sum**. Without the `tie` above, `fit.diagnostics()` reports
> them as not separately identified — which is the honest answer for that
> design.

---

## 4. Two stimulus dimensions

Numerosity **and** time (stimulus onset asynchrony), each with its own sensory
noise and its own prior. Parameter names gain the dimension suffix.

```python
data = btb.read_data("av2d.csv",
                     stimulus={"visual":   {"numerosity": "F", "time": "tF"},
                               "auditory": {"numerosity": "B", "time": "tB"}},
                     response={"visual":   {"numerosity": "rF"},
                               "auditory": {"numerosity": "rB"}},
                     missing=0, missing_dimension="numerosity")

model = btb.Model.from_data(data)
model.fix("mu_prior_time", 0.0)
model.set_param("sigma_visual_time", init=60.0, bounds=(1.0, 400.0))
fit = model.fit(data, n_sim=5000)
```

The time dimension has no responses, so it enters the causal inference but not
the likelihood — exactly as it should.

---

## 5. Simulation and parameter recovery

Simulation needs no data at all: declare an architecture, set parameters, choose
conditions.

```python
model = btb.Model(["visual", "auditory"], ["space"], response="continuous")
model.fix("p_common", 0.6)
model.fix("sigma_visual", 2.0)
model.fix("sigma_auditory", 9.0)
model.set_prior(mu=0.0, sigma=15.0)

sim = model.simulate([(-12, -12), (-12, 12), (12, -12), (12, 12)], n=5000)

sim.summary()        # per-condition mean, SD and mean p(C=1)
sim.to_frame()       # one row per simulated trial
sim.save_csv("simulated_trials.csv")
```

Because a simulation converts straight into a data set, a parameter recovery
study is four lines:

```python
truth = {"p_common": 0.6, "sigma_visual": 2.0, "sigma_auditory": 9.0,
         "mu_prior": 0.0, "sigma_prior": 15.0}

conditions = [(v, a) for v in (-12, -4, 4, 12) for a in (-12, -4, 4, 12)]
generated  = model.simulate(conditions, values=truth, n=80).to_data()
recovered  = btb.Model.from_data(generated).fit(generated, n_sim=3000)

for name, value in truth.items():
    print(name, value, "->", round(recovered.values[name], 3))
```

The same pattern answers "how many trials do I need?" — simulate at several
trial counts and watch the recovery error shrink.

---

## Fitting many participants

```python
data = btb.read_data("all_subjects.csv", stimulus=..., response=...,
                     subject="participant")

group = btb.Model.from_data(data).fit(data, by="subject", n_sim=10000)

print(group.summary())        # group mean, SD and 95% CI per parameter
group.to_frame()              # one row per participant
group.save_csv("parameters.csv")
```

Each participant is fitted independently (no pooling across participants) and
the group level is summarised afterwards.

---

## Validation

```python
# Can this design recover the parameters?
result = btb.recover(generator, conditions,
                     vary={"p_common": (0.1, 0.9), "sigma_visual": (1.0, 5.0)},
                     n_datasets=20, n_trials=60, n_sim=2000)
print(result.summary())
result.plot()

# Does the fitted model reproduce the data?
check = btb.posterior_predictive(fit)
print(check.summary())

# Did this fit go wrong?
print(model.fit(data, n_start=4).diagnostics()["text"])
```

---

## Model comparison

```python
full = btb.Model.from_data(data).fit(data)

null = btb.Model.from_data(data)
null.fix("p_common", 0.0)              # never integrate
null_fit = null.fit(data)

print(btb.compare({"BCI": full, "segregation only": null_fit}))
```
