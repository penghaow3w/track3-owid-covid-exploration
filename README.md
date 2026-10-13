# Track 3 — OWID COVID exploration and EMM null-distribution experiments

This repository records Penghao Wang's contributions to the Track 3 group project in **2AMM20 Research Topics in Data Mining**. It contains two separate stages: earlier OWID data preparation and pre-EMM exploration, and the newer search-aware null-distribution experiments using Lucas's EMM implementation.

**Current status (13 October 2026):** the L1-based experiments for K=1, K=2 and K=3 are completed, including 99 whole-country randomizations per K and subgroup-membership diagnostics. These are exploratory results, not established significance, fraud or causal conclusions. The full group project and comparison of additional quality measures are not complete.

## Start here

| What you want to inspect | File |
|---|---|
| Latest method and result explanation | [Null-distribution handoff](null_distribution/README.md) |
| Latest executed English notebook: code, all scores, figures and memberships | [owid_null_distribution_EN.ipynb](null_distribution/owid_null_distribution_EN.ipynb) |
| Same results with Chinese explanations | [owid_null_distribution_ZH.ipynb](null_distribution/owid_null_distribution_ZH.ipynb) |
| Earlier executed data-preparation walkthrough | [owid_pre_emm_walkthrough_en.ipynb](owid_pre_emm_walkthrough_en.ipynb) |
| Earlier preparation methods and reproduction instructions | [PRE_EMM_README_EN.md](PRE_EMM_README_EN.md) |

The newer notebooks do not replace the earlier preparation work. Read the stage descriptions below to avoid mixing data snapshots, targets and experiment designs.

## Stage 1 — Data preparation and pre-EMM exploration, 4–5 October 2026

### Purpose

Understand the OWID COVID data, decide how weekly observations and digit distributions should be constructed, and inspect descriptor coverage before connecting an automatic EMM search. This stage did **not** present final EMM discoveries.

### Work completed

- Inspected a fixed OWID compact snapshot containing **617,667 daily rows and 61 fields**.
- Audited country/date uniqueness, location types, missing values, zeros, calendar continuity and consistency between new and cumulative counts.
- Built country/region-by-calendar-week observations, with explicit checks for incomplete weeks, missing, negative, nonfinite and noninteger target values. Missing daily targets were not replaced with zero.
- Implemented general leading-K-digit extraction without zero-padding, audited digit availability and prepared fixed K=1/K=2 cohorts.
- Audited descriptor coverage and prepared country-based descriptor quartiles shared across K=1/K=2.
- Compared **TV, base-2 Jensen–Shannon divergence and Hellinger distance** on **29 predefined single-condition rules per K**. These were planned-rule comparisons, not the later automatic beam-search experiments.
- Examined minimum-support sensitivity, equal-country versus equal-week weighting, and year-specific reporting coverage.
- Produced executed notebooks, ten numbered walkthrough figures, meeting material and a reproducible preparation package.

### Earlier results and their scope

The preparation report recorded 45,170 positive complete weeks, a K=1 core cohort of 44,567 weeks across 226 locations, and a K=2 cohort of 37,590 weeks. Among its predefined comparisons, year 2026 ranked highest under equal-week and equal-country TV scoring. Reporting coverage shrank in later years, so this was not evidence of fraud or a confirmed anomaly.

These figures belong to the **earlier snapshot and weekly new_cases preparation**. They must not be substituted for the later joint cases/deaths experiment counts below.

### Earlier files

- [owid_analysis_en.ipynb](owid_analysis_en.ipynb): initial executed data exploration.
- [build_exploration.py](build_exploration.py): initial processing and plotting implementation.
- [OWID_meeting_brief_en.html](OWID_meeting_brief_en.html): historical meeting brief; download/open locally if GitHub does not render HTML.
- [preprocessing_decisions.md](preprocessing_decisions.md): historical provisional decisions and questions, not a specification of today's experiment.
- [owid_pre_emm_walkthrough_en.ipynb](owid_pre_emm_walkthrough_en.ipynb): the fuller 5 October walkthrough.
- [pre_emm_reproducible_2026-10-05.zip](pre_emm_reproducible_2026-10-05.zip): scripts, notebook and small outputs with their directory structure.

The earlier ZIP excludes the large raw snapshot. Its instructions specify `data/raw/compact_2026-10-04.csv` and SHA256 `7481c676492771e8425b118eaa983e987dd7312989ddcf7c67de09e635c53abc`. A fresh OWID download may differ from that fixed snapshot.

## Stage 2 — Search-aware null distribution and result diagnosis, 13 October 2026

### Purpose and division of work

The EMM objective is to find subgroups whose **joint leading-digit distribution differs from the complement**, not merely from theoretical Benford frequencies.

Lucas supplied the beam-search EMM framework and L1 quality measure. Penghao's work adds the whole-country randomization wrapper, repeated full-search maximum baseline, eligibility and country-coverage audits, saved experiment results, tests and subgroup diagnoses. The inspected Lucas snapshot is acknowledged as upstream work; this repository does not claim authorship of his EMM framework or synchronization with his latest branch.

### Data and missing-value policy

Input is `covid_preprocessed.csv` from Lucas's downloaded repository snapshot. It contains **61,661 rows and 239 country/region codes**, not the earlier daily input. The randomization experiment retains **233 codes with the same complete 261-week calendar**, giving **60,813 rows**, from **6 January 2020 to 30 December 2024**. Six incomplete calendars are excluded and recorded.

- Targets: weekly `new_cases` and `new_deaths`, modeled jointly.
- Target NaNs are preserved, not filled with zero. A row counts only if both targets yield valid digit prefixes; zero, negative, infinite and missing targets do not contribute.
- `pad=False`: K=1 requires both targets >=1, K=2 requires >=10, and K=3 requires >=100. Jointly valid counts are **25,206**, **15,405** and **6,339** respectively.
- Numeric descriptor NaNs do not satisfy interval rules; countries are not removed through blanket complete-case filtering.
- Lucas's upstream vaccination preprocessing is retained. Our no-target-imputation policy does not mean the entire upstream dataset is unimputed.

### Descriptors and fixed search settings

All eight substantive descriptors are included: `continent`, `population`, `population_density`, `median_age`, `life_expectancy`, `gdp_per_capita`, `diabetes_prevalence`, and `people_vaccinated_per_hundred`.

Identifiers, calendar date, week completeness and target columns are not used as descriptors. Settings are **beam width=10, depth=2, numeric bins=3, L1 quality, and at least 20 jointly valid records on each side**. No additional minimum country count is imposed; actual and effective country counts are reported. Beam search is heuristic, not exhaustive.

### How the null distribution is constructed

1. Run the observed-data EMM search and save its top results and maximum L1 score.
2. Randomly permute entire country target trajectories across the retained codes, moving cases, deaths and missingness together while preserving their internal dates.
3. Keep destination descriptors and calendar positions fixed.
4. Create a fresh EMM and repeat the same full beam-search procedure; record its maximum, not just the score of the originally selected subgroup.
5. Repeat 99 times for each K. Seed `20261013` gives matched country mappings across K=1/2/3. Fixed points are allowed; failed searches are not silently discarded or redrawn.
6. Compute the corrected exploratory tail fraction: `(exceedances + 1) / (99 + 1)`, using absolute tie tolerance `1e-12`.

This gives **300 searches in total**: one observed and 99 randomized searches for each of three digit settings.

### Results

| K | Observed maximum L1 | Random maxima reaching/exceeding observed, including ties | Corrected exploratory tail |
|---|---:|---:|---:|
| 1 | 1.1981416772554 | 3/99 | 0.04 |
| 2 | 1.9816692667706708 | 6/99 | 0.07 |
| 3 | approximately 2 | 95/99 | 0.96 |

These are **search-maximum** comparisons, not individually validated p-values for every displayed subgroup.

### What the best subgroups actually contain

- **K=1:** Oceania AND `4456.23 < gdp_per_capita <= 12134.9`. Five regions contain 1,305 weekly rows but only **22 jointly valid records**: Samoa 11, Tonga 5, Marshall Islands 4, Nauru 1, Tuvalu 1. In this subgroup, 1,282 rows contain at least one zero target and one contains at least one missing target.
- **K=2:** Oceania AND `21.8 < diabetes_prevalence <= 25.7`. Five selected regions again contain 1,305 rows, but only **21 valid records from two regions**: French Polynesia 14 and New Caledonia 7. Kiribati, Marshall Islands and Samoa contribute none. Twenty valid records are in 2020–2021 and one in 2022. All 21 occupy different digit pairs.
- **K=3:** North America AND `10.2 < diabetes_prevalence <= 12.7667`. There are **48 valid records from five contributing regions** among ten selected regions. The 48 distinct digit pairs share no pair with the complement, explaining L1 saturation at 2.

Actual memberships were recovered from reproduced searches and checked against the saved rules/scores. The notebooks include country tables, all contributing country-week values, invalid-reason counts, yearly coverage and digit-frequency comparisons.

### Interpretation and limitations

- Whole-country exchangeability is a modeling assumption, **not established by successful code execution**. Differences in country size, reporting and missingness may violate it.
- Vaccination varies over time and stays at the destination; randomization also breaks its association with the targets, not only static-country relationships.
- Best results depend on very few valid weeks. The >=20-record guard is not a guarantee of adequate estimation.
- K=3 has 810,000 joint cells and approximately **99.23% empty cells even across the full cohort**. Its high scores also occur under randomization, so higher K does not mean better anomaly detection.
- Without floating-point tie handling, K=3 would incorrectly appear to have a tail fraction of 0.06. Values differing only near machine precision around L1=2 are treated as ties, yielding **0.96**; raw values remain available for audit.
- B=99 has coarse 0.01 resolution and Monte Carlo uncertainty. No fraud, causal or formally established significance claim is made.

### Validation, files and reproduction status

Twelve unit tests passed. All 99 mappings per K, matching permutations across K, support counts, tail calculations and reproduction of the initial three-permutation pilot were checked. Both language notebooks were executed and saved with code, figures and results.

The GitHub `null_distribution/` folder currently contains its README and the English/Chinese executed notebooks. **The notebooks can be read on GitHub, but standalone rerunning requires the companion scripts, inputs, outputs and inspected snapshot. The full ZIP has not yet been uploaded to this folder as of this README update.** The prepared package is named `null_distribution_reproducible_2026-10-13.zip`; once uploaded, extract it and retain its directory structure before opening a notebook under `notebooks/`.

## What remains for the group project

- Review and report the assumptions behind the chosen whole-country randomization and the sparse effective support.
- Implement/select additional literature-supported quality measures in the main group repository, then rerun the corresponding randomized search baseline for each measure; L1 scores cannot be reused as another measure's null distribution.
- Compare and interpret subgroup results and incorporate appropriate limitations into the paper.

The current L1 null-distribution implementation and exploratory results are delivered; they do not mean the entire group paper or all evaluation tasks are complete.

## 中文导航

**之前（10月4–5日）**：数据检查、日转周、描述变量覆盖、前K位数字模型和29条预设规则比较；不是自动EMM结果。入口是 `owid_pre_emm_walkthrough_en.ipynb`。

**这次（10月13日）**：接入Lucas的EMM与L1，整国交换目标轨迹，K=1/2/3各99次重搜索，并检查成员、有效周和稀疏性。尾部比例为0.04/0.07/0.96；不能说已证明显著异常。中文结果见 [owid_null_distribution_ZH.ipynb](null_distribution/owid_null_distribution_ZH.ipynb)。

两个阶段的数据快照、目标和有效样本不同，不应混用数字。复现ZIP尚未出现在当前GitHub目录，需另行上传；只下载notebook可以看结果，但不能独立重跑。

