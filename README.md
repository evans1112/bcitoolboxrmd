# BCI Toolbox documentation

Source for the public [BCI Toolbox documentation](https://bci-toolbox.readthedocs.io/).
BCI Toolbox fits and simulates Bayesian causal inference models of multisensory
perception using a graphical interface or a reproducible Python API.

The documentation includes:

- installation and graphical-interface tutorials;
- one- and two-dimensional model fitting and simulation;
- the v0.3.0 programmatic workflow (`Data` → `Model` → `Fit`);
- parameter recovery, diagnostics, posterior-predictive checks, and plotting;
- a downloadable end-to-end tutorial notebook.

The Python package is maintained in
[evans1112/bcitoolbox](https://github.com/evans1112/bcitoolbox) and distributed
through [PyPI](https://pypi.org/project/bcitoolbox/).

## Build locally

```bash
python -m pip install -r docs/requirements.txt
sphinx-build -n -W -b html docs _build/html
```
