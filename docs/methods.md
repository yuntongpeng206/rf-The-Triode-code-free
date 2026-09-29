# Methods and review

## Preserved numerical method

For each current–voltage curve, select the inclusive voltage interval provided locally and fit I = m V + b using `numpy.polyfit(x, y, 1)`. A gm curve varies grid voltage at fixed anode voltage; a ga curve varies anode voltage at fixed grid voltage. The corresponding slope estimates the local derivative only where the selected interval is sufficiently linear.

The original notebook applies unweighted least squares separately to each curve, then calculates the arithmetic mean and sample standard deviation (`ddof=1`) across its slopes. These operations are retained. No instrument error model, weighted regression or automatic interval selection has been introduced.

The ratio summary is:

$$\mu=\frac{\overline{g_m}}{\overline{g_a}}.$$

The original independent propagation is written equivalently as:

$$s_\mu=\sqrt{\left(\frac{s_{g_m}}{\overline{g_a}}\right)^2+
\left(\frac{\overline{g_m}s_{g_a}}{\overline{g_a}^{\,2}}\right)^2}.$$

This derivative form agrees with the original positive-conductance calculation and remains defined at zero numerator. A zero denominator is marked unresolved. Missing across-curve scatter for a single curve remains undefined rather than being set to zero.

## What the spread means

The SD describes variation between fitted curves at different fixed bias conditions. It is not the standard error of the mean, an individual slope-fit error, or a complete experimental uncertainty. The ratio propagation treats these SDs as independent spread estimates; correlations, calibration uncertainty and interval-selection effects are not accounted for. A small ga can make the ratio unstable.

The report discusses local slope scatter, whereas the supplied code actually fits a line to each curve and takes SD across those fitted slopes. This package follows the code and documents the distinction. The physical identity mu = gm/ga is local to a shared operating point; the ratio of averages at different biases need not equal a single small-signal amplification factor.

## Deduplication and range selection

The source contains repeated code for multiple grids and alternative retest intervals. Several comments describe intervals different from the executable masks. Those values are not published or silently resolved here. The private fit-window table explicitly controls the calculation. Run separate labeled variants to compare choices. Original arrays, group labels, bias settings and numerical findings are not copied into the public package.

## Units

Use calibrated electrode voltages. If current is in A, slopes are A/V (siemens); other current units imply their corresponding conductance scale. A constant current offset changes the intercept but not the fitted slope. Voltage-dependent monitor offsets and nonlinear calibration can affect slopes. No monitor scaling or measurement uncertainty is invented.

## Source context

The supplied University of Manchester second-year laboratory handout *The Triode* was used for the parameter definitions. Teaching PDFs, the report and interview material are excluded. This project implements slope analysis only, not vacuum control or a complete physical model of thermionic emission.
