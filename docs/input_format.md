# Local input format

Create `private_data/` and fill copies of all three templates. No measured values or experimental fitting limits are included in the repository.

## measurements.csv

| Column | Meaning |
|---|---|
| group_id | Local label for a grid configuration, repeat or analysis variant |
| curve_id | Local scan label, unique within group and kind |
| kind | `gm` for anode current versus grid voltage; `ga` for anode current versus anode voltage |
| fixed_voltage_V | Actual anode voltage for gm; actual grid voltage for ga |
| swept_voltage_V | Actual grid voltage for gm; actual anode voltage for ga |
| current | Anode current in the single unit selected in settings.json |

Supply one row per measurement, at least two distinct swept voltages within each fit interval. Do not mix repeat scans or bias voltages within one curve ID. All required fields must be present and numeric values finite. Every group must contain both gm and ga curves. Use at least two curves of each type if a sample SD and propagated spread are needed. A single curve yields a slope, but its across-curve SD is undefined.

## fit_windows.csv

One row per group and kind: `group_id,kind,lower_voltage_V,upper_voltage_V`. Limits are inclusive, with lower < upper. Use the same group labels as the measurement file. The interval is applied to every curve of that kind in that group, matching the original workflow. Choose a common approximately linear region after inspecting your local curves.

To compare alternative intervals, use separate group labels and local copies of the same measurements with the different interval settings. The program does not choose a preferred interval or exclude measurements outside it from your input file; it only masks them during fitting.

## settings.json

Set `current_unit` to `A`, `mA`, `uA` or `monitor_unit`. The last label means an uncalibrated current-monitor reading; the slopes must then not be called conductance in siemens. Consistent multiplicative current scaling cancels from the ratio, but differing channel gains do not.

Both voltage columns must contain actual electrode voltages in volts, after monitor calibration. The code does not infer conversions from column labels or original notebook variable names.

## Local output

`private_outputs/curve_slopes.csv` contains each curve's slope, intercept and fit interval. `group_summary.csv` contains means, sample SD, counts, the conductance ratio and propagated spread. These reveal experimental findings and should remain local.
