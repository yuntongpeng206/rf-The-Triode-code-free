# Triode Characteristic Analysis

Python analysis of triode current–voltage characteristics to estimate mutual conductance, anode slope conductance and an amplification-factor summary.

**This is a code-only repository.** Experimental measurements, fit-window values, derived results, original notebooks, reports, interview slides and teaching PDFs are not distributed. All templates are empty and the notebook has no saved outputs.

## Workflow

1. Supply local anode-current scans versus grid voltage at fixed anode voltage.
2. Supply local anode-current scans versus anode voltage at fixed grid voltage.
3. Choose a linear fitting interval for each group and scan type.
4. Fit straight lines, average slopes and compute their sample standard deviations.
5. Compute the ratio of mean mutual conductance to mean anode conductance.

$$g_m=\left.\frac{\partial I_a}{\partial V_g}\right|_{V_a},\qquad
 g_a=\left.\frac{\partial I_a}{\partial V_a}\right|_{V_g}.$$

The script retains the original summary method, $\mu_{\mathrm{summary}}=\overline{g_m}/\overline{g_a}$. For a physical small-signal amplification factor, both derivatives should refer to the same operating point; averages across different bias conditions are descriptive summaries.

## Run locally

Python 3.10 or later:

```bash
python -m pip install -r requirements.txt
python src/analysis.py
```

Without data, the script prints setup instructions. Create `private_data/`, copy and complete the three files in `templates/`, then run again. Tables are written to `private_outputs/` and are not printed or embedded automatically.

```bash
jupyter notebook notebooks/triode_analysis.ipynb
```

## Files

| Path | Purpose |
|---|---|
| `src/analysis.py` | Shared linear-fit and aggregation workflow |
| `notebooks/triode_analysis.ipynb` | Output-free notebook entry point |
| `templates/` | Empty measurement, fitting-window and unit templates |
| `docs/input_format.md` | Input definitions and units |
| `docs/methods.md` | Equations, preserved decisions and limitations |

## About this version

Repeated notebook blocks are refactored into a common function. Original unweighted linear fits, arithmetic means, sample SD and independent ratio propagation are retained. Alternative fitting intervals are local configuration choices; no original interval or grid result is selected or disclosed. Input validation, unit labels and undefined-case handling are added. This is a ChatGPT-assisted refactor of the author's code, not an unchanged original notebook.

Fit spread is not a complete measurement uncertainty. Monitor voltages must be calibrated before analysis; no instrument scale factors are assumed. See [methods](docs/methods.md).

Private directories are ignored by Git, but ignore rules do not remove tracked files or prevent manual website uploads. Clear notebook outputs before sharing any locally executed copy.
