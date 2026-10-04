# OWID COVID weekly digit-distribution exploration

## English

This folder contains the pre-EMM exploration prepared for the next Group 6 meeting. It does **not** present anomaly, significance, fraud, or final EMM results.

### Current design

- Analytical unit: country/region × complete calendar week.
- Target: weekly sum of daily `new_cases`.
- Missing daily values are not replaced with zero.
- A general parameter `K` extracts the first K significant digits without zero-padding.
- For this COVID dataset, K=1 is the primary setting and K=2 is a practical extension. K=3 remains implemented as a coverage sensitivity check.
- Candidate descriptors include continent, year, population, population density, median age, life expectancy and GDP per capita. Cumulative vaccination counts are not proposed for the first model because they are time-varying and highly incomplete.

### Completed checks

- Audited 617,667 daily rows and 61 fields.
- Checked country-date uniqueness, location types, missing values, zero values, date continuity, and arithmetic consistency between new and cumulative counts.
- Built the complete country-week table and audited candidate descriptor coverage.
- Verified that the raw snapshot remained unchanged.

### Files

- `owid_analysis_en.ipynb`: English notebook with actual processing code, tables and plots.
- `owid_analysis_zh.ipynb`: Chinese study version with identical code and outputs.
- `OWID_meeting_brief_en.html`: English meeting brief for group members and Bart.
- `OWID_meeting_brief_zh.html`: Chinese study brief.
- `build_exploration.py`: reproducible preprocessing and plotting program.
- `results/`: small coverage summaries only.
- `figures/`: selected meeting figures.
- `preprocessing_decisions.md`: provisional decisions and questions for Bart.

The large raw CSV is intentionally not committed. Download it from the [OWID COVID compact dataset](https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv) and save it as `data/raw/compact_2026-10-04.csv` in the local project if reproduction is required.

### Questions for the meeting

1. Confirm country-week `new_cases` as the analytical unit and target.
2. Decide whether numerical descriptors should be continuous, predefined quantile bins, or both.
3. Decide whether GDP missingness is acceptable and whether vaccination descriptors should be deferred.
4. Confirm K=1 as the primary COVID representation and K=2 as secondary.
5. Define the quality measure comparing a subgroup digit distribution with its complement.
6. Agree on evaluation and multiple-search control before interpreting subgroups.

## 中文

这个文件夹包含 Group 6 下次会议前的 OWID 数据探索。它**不包含**正式异常、显著性、欺诈或最终 EMM 结论。

### 当前设计

- 分析单位：国家/地区 × 完整日历周。
- 目标：每日 `new_cases` 的周总数。
- 日缺失值不填零。
- 通用参数 `K` 提取正整数的前 K 位有效数字，不补零。
- 对 COVID 数据，K=1 为主要设置，K=2 为实用扩展；K=3 保留为覆盖率敏感性检查。
- 候选描述变量包括大洲、年份、人口、人口密度、年龄中位数、预期寿命和人均 GDP。累计疫苗数随时间变化且缺失很多，暂不建议放进第一个模型。

### 已完成检查

- 审计 617,667 条日记录和 61 个字段。
- 检查 country-date 唯一性、地点类型、缺失、零值、日期连续性，以及新增数和累计数的算术一致性。
- 构建完整国家—周数据，并审计候选描述变量覆盖率。
- 验证原始快照没有被修改。

### 文件说明

- `owid_analysis_en.ipynb`：英文完整代码、表格和图。
- `owid_analysis_zh.ipynb`：相同代码和结果的中文学习版。
- `OWID_meeting_brief_en.html`：给组员和 Bart 的英文会前材料。
- `OWID_meeting_brief_zh.html`：中文复习材料。
- `build_exploration.py`：可复现的预处理和绘图程序。
- `results/`：小型覆盖统计。
- `figures/`：精选会议图。
- `preprocessing_decisions.md`：临时预处理建议和待 Bart 确认的问题。

大型原始 CSV 不上传。需要复现时，从 [OWID COVID compact dataset](https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv) 下载，并在本地项目中保存为 `data/raw/compact_2026-10-04.csv`。

下一步是让 Bart 确认分析单位、描述变量处理、K 的主要设置和质量指标，然后再连接 EMM。
