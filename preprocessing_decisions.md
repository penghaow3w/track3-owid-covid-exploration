# OWID weekly exploration: candidate preprocessing decisions

Date: 2026-10-04

## Evidence

The candidate table has 81,936 country-week rows. Weekly `new_cases` is nonmissing in 80,142 rows (2.190% missing). A positive complete weekly total exists for 45,170 rows.

Descriptor coverage:

| Descriptor | Missing country-week rows | Initial decision |
|---|---:|---|
| population | 0.483% | Keep as a country-level descriptor; do not repeat it as an independent observation. Consider population quartiles only after fixing the country reference date. |
| median_age | 0.483% | Keep as a country-level descriptor. |
| life_expectancy | 0.483% | Keep as a country-level descriptor. |
| population_density | 2.182% | Keep; inspect its long tail and use log scale for plots. Any transformation must be agreed before EMM. |
| gdp_per_capita | 16.039% | Candidate only; compare complete-case coverage and avoid silently dropping countries. |
| total_vaccinations | 78.417% | Do not use as a primary descriptor in the first model; it is cumulative and time-varying with very high missingness. |

## Proposed exploratory rules for discussion with Bart

1. Use country-week `new_cases` as the main target. Keep only complete weeks and positive totals when extracting digits. Do not impute missing cases as zero.
2. Use `continent` and `year` as simple, interpretable descriptors.
3. Use population, median age, life expectancy and population density as candidate descriptors. For numerical descriptors, compare quantile bins against continuous/log-plotted versions. Do not choose cut points because they produce a high TV.
4. Treat GDP per capita as a secondary candidate because 16% of candidate rows lack it. Report the exact missingness rule if used.
5. Exclude cumulative vaccination counts from the initial descriptor set unless Bart specifically wants a time-varying descriptor experiment. The missingness is about 78% and the variable is not a fixed country characteristic.
6. Use first digit as the primary digit representation and first two digits as a secondary representation. First-three-digit results are optional because only 27,653 rows have at least three digits.
7. Do not run EMM or call a subgroup anomalous until Bart approves the target, descriptor bins and quality measure.

These are candidate rules, not final research decisions. They are meant to make tomorrow's discussion concrete.
