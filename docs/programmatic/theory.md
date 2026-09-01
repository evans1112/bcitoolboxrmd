# The model, as implemented

This page states exactly what the code computes. It is the reference for anyone
who needs to describe the toolbox in a methods section.

---

## 1. Generative model

For each stimulus dimension `d`, a latent source is drawn from a Gaussian prior

```
s_d ~ N(μ_P,d , σ²_P,d)
```

Under a **common cause** (`C = 1`) all modalities share one source; under
**independent causes** (`C = 2`) each modality `m` has its own, drawn from the
same prior. Every modality receives a noisy measurement

```
x_md ~ N(s_md + b_md , σ²_md)
```

where `b_md` is a constant sensory bias (`bias_<modality>`, fixed at 0 by
default).

The prior probability of a common cause is `p_common`.

---

## 2. Causal inference

Marginalising the latent sources analytically gives closed-form evidences.
With `u_m = x_md − μ_P,d` and `a_m = 1/σ²_md`, over the `k` modalities present
on dimension `d`:

```
A = Σ a_m ,  S = Σ a_m u_m ,  Q = Σ a_m u²_m

log p(x_d | C=1) = −½ [ k·log 2π + Σ log σ²_md + log(1 + σ²_P,d·A)
                        + Q − σ²_P,d·S² / (1 + σ²_P,d·A) ]

log p(x_d | C=2) = Σ_m log N(x_md ; μ_P,d , σ²_md + σ²_P,d)
```

The first line is the density of a multivariate normal with covariance
`diag(σ²) + σ²_P·11ᵀ`, expanded with the matrix determinant lemma and the
Sherman–Morrison identity. Evidence multiplies across dimensions, so

```
p(C=1 | x) = logistic( Σ_d [log p(x_d|C=1) − log p(x_d|C=2)]
                       + log( p_common / (1 − p_common) ) )
```

Three consequences are worth stating explicitly.

- **Any number of modalities.** The formula holds for any `k`, so trimodal
  models work through the same code path as bimodal ones.
- **Unimodal trials need no special case.** With `k = 1` the two evidences are
  algebraically identical, so the posterior equals `p_common`, the fused and
  segregated estimates coincide, and every decision strategy returns the same
  response. The classic implementation approximated this by setting the absent
  modality's noise to a very large number (σ = 1000); here the modality is
  simply dropped, which is exact.
- **Log space.** Working with log evidences avoids the underflow that affects a
  direct product of densities when the two signals are far apart.

---

## 3. Estimates

Both estimates are precision-weighted means:

```
ŝ_C=1,d   = ( Σ_m a_m x_md + μ_P,d/σ²_P,d ) / ( Σ_m a_m + 1/σ²_P,d )

ŝ_C=2,md  = ( a_m x_md + μ_P,d/σ²_P,d ) / ( a_m + 1/σ²_P,d )
```

---

## 4. Decision strategies

| Strategy | Response of modality `m` |
| --- | --- |
| `averaging` | `p(C=1\|x)·ŝ_C=1 + (1 − p(C=1\|x))·ŝ_C=2,m` |
| `selection` | `ŝ_C=1` if `p(C=1\|x) > p_cutoff`, else `ŝ_C=2,m` |
| `matching` | `ŝ_C=1` if `p(C=1\|x) > u`, `u ~ U(0,1)` drawn per trial, else `ŝ_C=2,m` |

`p_cutoff` defaults to 0.5 and can be freed like any other parameter.

---

## 5. Response model

The perceptual estimate is turned into a response by, in order:

1. adding Gaussian response noise with SD `sigma_motor_<modality>` (0 by default);
2. replacing the response with a uniform draw over the response support with
   probability `lapse` (0 by default);
3. for discrete tasks, snapping to the nearest allowed level.

---

## 6. Likelihood

**Discrete responses** — multinomial over the levels, using the observed counts
`n_ck` in condition `c`:

```
log L = Σ_c Σ_k n_ck · log[ (1 − ε)·p_ck + ε/K ]
```

with `K` levels and `ε = 0.001`. (The classic implementation reconstructed the
counts as `n_trials // (N² − 1)`, which is only correct when every condition has
the same number of trials and that number divides evenly; the observed counts
are used here.)

**Yes/no judgements about the causal structure** — Bernoulli. The observer
reports a common cause when `p(C=1 | x)` exceeds a criterion (`unity_criterion`,
0.5 by default), or with probability equal to `p(C=1 | x)` under the
`"matching"` rule. This covers unity judgements, body-ownership reports and
"simultaneous / not" judgements.

**Continuous responses** — Gaussian kernel density estimate of the simulated
responses, evaluated at the observed ones:

```
log L = Σ_i log[ (1/J) Σ_j N(y_i ; ŷ_j , h²) ]
```

computed with a log-sum-exp for stability. The bandwidth `h` is derived from the
**within-condition** spread of the observed responses of that modality, with the
number of simulated samples in the rate — see
[`responses.md`](responses.md#how-the-bandwidth-is-chosen-and-why-it-matters)
for why this matters.

---

## 7. Validation

### Against the classic implementation

The engine is checked against `BCIbox.prod_gaus` / `prod3gauss` and the classic
`Sc`, `Snc1`, `Snc2` expressions:

| Quantity | Maximum absolute difference |
| --- | --- |
| `p(x \| C=1)` | 2.2 × 10⁻¹⁹ |
| `p(x \| C=2)` | 6.5 × 10⁻¹⁹ |
| `p(C=1 \| x)` | 2.2 × 10⁻¹⁶ |
| fused estimate `ŝ_C=1` | 1.8 × 10⁻¹⁵ |
| segregated estimate `ŝ_C=2` | 0.0 |

### Parameter recovery

Continuous localisation, 16 conditions × 80 trials, `n_sim = 3000`, Powell:

| Parameter | True | Recovered | Error |
| --- | --- | --- | --- |
| `p_common` | 0.60 | 0.620 | +2.0% |
| `sigma_visual` | 2.00 | 1.951 | −2.5% |
| `sigma_auditory` | 9.00 | 8.839 | −1.8% |
| `sigma_prior` | 15.0 | 15.03 | +0.2% |
| `mu_prior` | 0.0 | −2.48 | see note |

Discrete numerosity, 15 conditions × 60 trials, prior parameters fixed:

| Parameter | True | Recovered |
| --- | --- | --- |
| `p_common` | 0.65 | 0.628 |
| `sigma_visual` | 0.45 | 0.441 |
| `sigma_auditory` | 0.90 | 0.896 |

> **Note on the prior parameters.** `mu_prior` and `sigma_prior` are only weakly
> identified in designs where the prior barely influences the responses. In the
> localisation example above the prior carries 1.7% of the weight for the visual
> estimate, so `mu_prior` scatters over several units across replications
> (−2.48, 0.29, 0.78, 0.80 for four data sets generated from `mu_prior = 0`)
> without bias. In discrete numerosity designs with three levels, `mu_prior` and
> `sigma_prior` trade off against each other. This is a property of those
> designs, not of the estimator; the classic GUI addresses it by fixing
> `sigma_prior` at a very large value, i.e. a flat prior. Use
> `model.set_prior(mu=..., sigma=...)` to do the same, and check
> `fit.optimization.converged_consistently` with `n_start > 1`.

Strategy recovery: data generated with `averaging` are correctly identified
(ΔBIC ≈ 50 over `matching`, ≈ 79 over `selection`).

### Across paradigms

Every paradigm below was generated from known parameters and fitted back; the
figures are the recovered values against the true ones.

| Paradigm | Check |
| --- | --- |
| Visuo-proprioceptive reaching | `p_common` 0.74 (0.70), `sigma_vision` 0.49 (0.50) |
| Size–weight illusion | `sigma_size` 0.72 (0.80), `sigma_weight` 0.28 (0.30) |
| 9-point rating scale | `sigma_visual` 0.79 (0.80) |
| Rubber-hand ownership | `P(illusion)` peaks at synchrony and falls symmetrically: 0.26, 0.63, 0.84, **0.93**, 0.86, 0.65, 0.26 across ±500 ms |
| Localisation + unity judgement | `sigma_visual` 1.96 (2.00) |
| Two dimensions, both reported | `sigma_visual_space` 2.01 (2.00), `sigma_visual_time` 27.9 (30.0) |
| Trimodal | `sigma` 2.0 / 7.3 / 4.7 (2 / 8 / 5) |
| Unbalanced conditions (5–100 trials) with 20% missing responses | `p_common` 0.58 (0.60) |
| Mixed scales (degrees and milliseconds in one model) | 1.43 (1.50) and 37 (40) |

Response scale does not matter: the same design fitted in milliseconds, pixels
or 0–1 units gives the same relative errors, because the parameter defaults are
derived from the data.
