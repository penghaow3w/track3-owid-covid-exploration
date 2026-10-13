OWID search-aware null distribution: 99 whole-country permutations
1. Objective and delivered work
We use Lucas's inspected EMM snapshot to search for subgroups whose joint leading-digit distribution of weekly new cases and new deaths differs from the complement. We rerun the same beam search after every randomization and retain its maximum score. This is not a comparison against theoretical Benford frequencies and not a fixed-subgroup-only test.
K=1, 2 and 3 each have one observed-data search and 99 randomized searches: 300 searches in total. Results are exploratory: cross-country exchangeability has not been established, so the corrected tail fractions are not validated significance claims.
2. Input, cohort and missing values
Input is Lucas's preprocessed covid_preprocessed.csv, not untouched daily OWID data. The source has 239 country/region codes and 61,661 rows. We keep the 233 codes sharing the full 261-week calendar (60,813 rows), 2020-01-06 to 2024-12-30. Six incomplete calendars are excluded and listed below. Complete calendars do not imply complete targets.
We do not replace missing case/death targets with zero. A row contributes to the joint model only if both targets yield valid leading digits. Missing, zero, negative and infinite values are excluded from digit counting, not silently deleted from the whole table. pad=False requires both targets >=1, >=10 and >=100 for K=1,2,3 respectively. Different K therefore use different samples. Numeric descriptor NaNs satisfy no interval condition; we do not remove whole countries for missing numeric descriptors. Vaccination was previously processed by Lucas; our no-imputation policy must not be confused with an entirely unimputed upstream dataset.
3. Descriptors and search settings
All eight substantive descriptors: continent, population, population_density, median_age, life_expectancy, gdp_per_capita, diabetes_prevalence, people_vaccinated_per_hundred. Identifiers, date, days and the two targets are excluded as descriptors.
Beam width=10; depth=2 (up to two conditions); n_bins=3 (numeric quantile intervals recomputed inside each parent; duplicates may reduce the number of bins). Quality is L1 between subgroup and complement joint distributions. Both sides require >=20 jointly valid records. There is no additional country-count threshold; country coverage is reported. Twenty records do not guarantee adequate estimation of 8,100 cells. Beam search is heuristic, not exhaustive.
4. Randomization and calculation
Fix data, features and settings; seed=20261013.
Search observed data and save the top ten results and maximum.
Uniformly permute whole-country target trajectories across the 233 country/region codes. Move cases, deaths and missingness together, aligned by date.
Keep destination descriptors and calendar positions fixed; create and run a fresh EMM search.
Save its maximum and destination/source mapping; repeat 99 times without silently dropping failed searches or redrawing.
Corrected tail fraction = (number of randomized maxima >= observed maximum + 1)/(99+1).
The same seed gives matched permutations for all K. Fixed points are allowed. Absolute tie tolerance=1e-12 handles floating-point L1 saturation near 2; raw strict-comparison counts are retained for auditing.
The null requires invariance to exchanging whole target trajectories across countries conditional on retained descriptors. This is unproven. Country size, reporting and missingness may violate it. Time-varying vaccination stays at the destination, so its association with targets is also broken: this is not exclusively a static-country-attribute test. A new quality measure needs its own randomized search maxima.
6. Interpretation and limitations
Red line: observed search maximum. Histogram: randomized search maxima. Small tail fractions mean rarity under this particular randomization design, not fraud, causality or automatically valid statistical significance. B=99 gives resolution 0.01 and Monte Carlo uncertainty. We test the search maximum; we have not assigned independently valid p-values to all top-ten rules.
Best K=1 subgroup has 22 valid records; K=2 has 21 and only two contributing regions. K=3 has 810,000 cells and saturation near 2. These limitations are reported rather than retrospectively changing thresholds.
Engineering incident: after all 99 K=1 scores were saved, NumPy int64 prevented JSON summary serialization. We converted to Python int and recovered the summary from complete checkpoints without rerunning or replacing permutations. Recovery and timing provenance are recorded in summary.json. A validation import-path issue was also fixed before successful execution.
7. Files and reproduction
This portable package contains notebooks/, scripts/, outputs/, vendor/ and inputs/. Open notebooks/owid_null_distribution_EN.ipynb or the Chinese counterpart. The display notebook reads saved outputs and does not automatically trigger 300 searches.
scripts/run_owid_99.py reproduces all three K experiments. scripts/explain_best_subgroups.py reproduces the observed searches to extract real memberships and diagnose the results. scripts/verify_owid_99.py checks all 99 scores, mappings, counts, matched K permutations and reproduction of the original three-shuffle pilot. Run tests with python -m unittest discover -s scripts -p 'test_*.py'. Dependencies are in requirements.txt.
Inputs include a compact ZIP containing the exact preprocessed source CSV and a country-name mapping used only for labels. CSV SHA256: 81b7b6668fc75581300143324e75583281b124b3e0411c079407cf60f0849274. Vendor code is Lucas's inspected local snapshot, not a claim about his latest remote branch; retain attribution and applicable upstream terms. Full implementation follows.
8. Completed experiments and conclusions
All three K experiments have 99 whole-country permutations and complete repeated beam searches: 300 searches total. All corresponding mappings match across K.
K	Observed maximum L1	Exceedances including ties / 99	Corrected exploratory tail
1	1.1981416772554	3	0.04
2	1.9816692667706708	6	0.07
3	approximately 2	95	0.96
K=1 best rule: Oceania AND 4456.23 < gdp_per_capita <= 12134.9. K=2: Oceania AND 21.8 < diabetes_prevalence <= 25.7. K=3: North America AND 10.2 < diabetes_prevalence <= 12.7667. Original descriptor units are retained.
K=3 randomized maxima range from 1.9996823379923763 to approximately 2; runtime approximately 746.5 seconds. Across the full cohort K=3 has 6,339 valid records and about 99.23% empty joint cells. A score near 2 is not evidence of superior detection. No claim of country exchangeability, fraud detection or formally established significance is made.
K=3 floating-point ties: important
95/99 randomized maxima equal or exceed the observed maximum with absolute tolerance 1e-12, giving (95+1)/100=0.96. Strict floating-point comparison gives only 5 exceedances and 0.06; that result is distorted by machine-precision differences near the theoretical L1 bound 2. Raw values remain in summary.json for auditing, but must not be interpreted as genuine rank evidence.
K=3 finished at 16:27 CEST on 2026-10-13. All mappings, counts, tails and pilot reproduction were verified; twelve unit tests passed. GitHub upload has not been performed.
9. Membership and high-score diagnosis
We rerun each original search to obtain its actual membership indices and assert agreement with the saved best rule and score. No random experiments are rerun and no eligibility thresholds changed. Actual indices avoid errors from parsing displayed quantile boundaries.
Country names come from a local OWID code-to-name mapping used only for labels. We show every contributing country-week with values and extracted prefixes. The chart shows only the twelve digit pairs with the largest L1 contributions; complete occupied pairs are saved in all_occupied_digit_pairs.csv. The year chart counts valid country-week records, not cases or deaths.
Invalid-reason categories are mutually exclusive with priority: missing, infinite, negative, zero, below the K-digit threshold, then valid. They are not independent per-target counts. These are preprocessed weekly values: zero may reflect reporting practices and cannot always be interpreted as no actual disease.
Diagnosis conclusions
K=1: five regions have 1,305 rows but only 22 jointly valid records (1.69%). 1,282 rows contain at least one zero and one contains at least one missing target. Samoa contributes 11 valid records; Tonga five, Marshall Islands four, Nauru one, Tuvalu one. The result describes these 22 records, not a stable five-year regional epidemic feature.
K=2: five selected regions, but only New Caledonia (seven records) and French Polynesia (fourteen) contribute. Kiribati, Marshall Islands and Samoa have zero eligible records. Twenty records are in 2020–2021, one in 2022, none in 2023–2024. All 21 records occupy different digit pairs. Twenty pairs also occur in the complement, yet overlap probability mass is only about 0.00917, explaining L1 approximately 1.9817. Shared cells do not imply similar frequencies.
K=3: 48 valid records occupy 48 unique pairs and share no pair with the complement. Overlap mass=0, so L1=2 within floating-point precision. This directly explains saturation; the 0.96 randomized tail also shows no rarity.
These are descriptive post-search diagnoses, not new independent tests. They do not prove zeros/missingness are the sole cause or establish fraud or causality. No country threshold was added. Full selected rows, all valid rows, country coverage, invalid reasons, annual counts and digit pairs are saved in outputs/best_subgroup_explanations_2026-10-13/k1, k2 and k3.



///
OWID null distribution — 99 whole-country permutations
1. 目的与本次交付
使用 Lucas 的原始 EMM 快照，寻找病例与死亡联合数字分布不同于补集的 subgroup。每次随机化后重新运行同样的 beam search，取搜索最高分，构造考虑搜索选择过程的随机参照。这里不是与 Benford 理论频率比较，也不是只重复打分原来那个 subgroup。
本次 K=1、2、3 各运行原始搜索一次、随机重搜索99次，共300次搜索。K=3按用户要求也完成相同规模实验。此处是探索性结果；国家间可交换性尚未证明，尾部比例不能当作已验证的正式显著性结论。
2. 输入、筛选和缺失值
输入为用户下载的 Lucas ZIP 中 covid_preprocessed.csv，不修改该CSV或Lucas源代码。全表239个国家/地区、61661行；本实验保留233个具有相同261周完整日历的地区，共60813行，日期2020-01-06至2024-12-30。6个不完整日历地区的排除原因见下表。完整日历仅代表日期位置完整，不表示目标无缺失。
目标new_cases和new_deaths保留NaN，不填0。仅两者都能提取有效数字的行参与联合分布，零、负数、无穷值、缺失值均不能计入。pad=False：K=1要求两者≥1，K=2要求两者≥10，K=3要求两者≥100。因此不同K会使用不同有效样本，高分不能直接跨K比较。数值描述变量缺失的行不满足该数值区间规则，但没有因此完整案例删掉整国。疫苗列此前已由Lucas预处理，不能把本阶段不填补误说为原始数据从未填补。
3. 描述变量与搜索设置
全部8个实质描述变量：continent（洲）、population（人口）、population_density（人口密度）、median_age（年龄中位数）、life_expectancy（预期寿命）、gdp_per_capita（人均GDP）、diabetes_prevalence（糖尿病患病率）、people_vaccinated_per_hundred（每百人已接种人数）。标识code、日期week_start、周完整性days及两个目标不纳入描述变量。
width=10：每层保留10个候选；depth=2：最多两个描述条件；n_bins=3：连续变量按分位数分三段，重复边界可能减少段数，并在父subgroup内重新分箱。质量度量为L1，模型是两个目标的联合前K位数字分布，比较对象是补集。双方至少20条联合有效记录；不设国家数门槛，但显示国家数与有效国家数。该20条阈值不代表足以支持8100格子的估计。beam search是启发式，不是穷举。
4. 交换方法与计算步骤
①固定筛选后的数据、描述变量、目标、搜索参数及随机种子20261013。②原始数据完整搜索，保存top10及最高分。③在233个地区间随机排列整段目标记录，把病例、死亡和缺失模式一起按相同日期送到目的地区。④保持目的地区描述变量、行位置、日期不变，重新创建EMM并搜索。⑤保存本次最高分与交换映射。⑥重复99次，计算(达到或超过原始最高分的次数+1)/(99+1)。每次都保留结果，不静默丢弃失败搜索或重抽。
三种K用相同种子，对应同一批交换映射。允许国家交换到自己，这是均匀排列的一部分。浮点并列采用绝对容差1e-12，保留未经容差处理的次数供核查。每种度量或搜索设置必须有自己的随机参照，不能直接套用本次L1的分布。
零假设要求整段目标轨迹在地区描述信息之间可交换。该假设没有因代码运行成功而得到证明。国家间规模、报告方式、缺失模式差异可能使其不合理。疫苗描述变量随周变化并留在目的位置，交换也打破它与目标的时间对应，因此本实验不是只检验固定国家属性的关联。
6. 如何解释结果
红线表示原始搜索最高分，柱形图表示随机数据重新搜索得到的最高分。尾部比例小表示相对于本次指定的随机机制更罕见，不自动证明真实世界异常、数据造假或因果关系。B=99分辨率为0.01，结果仍有蒙特卡洛波动。这里评估的是搜索最高分，不是给每个top10规则都计算了独立有效的p值。
K=1最佳规则有22条有效记录，分布有81格；K=2最佳规则有21条有效记录且仅2个地区贡献有效记录，分布有8100格。这些是重要解释限制，不是未经约定新增排除门槛。K=3联合分布有810000格子，原始与随机分数均约2，之前浮点细微差别已按并列处理，不能作为显著性证据。下一步交给Lucas讨论随机机制与质量度量，而不是盲目增加次数。
本次遇到的工程问题：K=1的99次分数都已写入检查点，但保存summary时NumPy int64无法直接JSON序列化；已改为Python int，并从已保存的99次记录恢复汇总与图，不重跑、不抽换随机排列。summary.json记录了恢复说明及按最终检查点时间计算的耗时。该问题不改变分数。
7. 文件位置与复现
本地根目录：本交付包根目录。JupyterLab 8892：evaluation → notebooks → owid_null_distribution_99.ipynb。脚本：evaluation → scripts → run_owid_99.py 与 owid_real_pilot.py。每种K结果在evaluation → outputs → owid_all_descriptors_k1_B99_2026-10-13及k2、k3对应目录。包含settings.json（参数、源哈希、开始时间）、summary.json（结果、结束时间）、cohort.csv、descriptor_audit.csv、observed_subgroups.csv、randomized_maxima.csv、99份mapping CSV及search_maximum_baseline.png。旧3次试跑与旧笔记本保留。
上面只读取已有结果，不自动触发200次搜索。下面展示完整实际运行实现及调用脚本；核心搜索和交换逻辑随后展示。
8. K=3追加实验与完整结论
K=1、2、3现在均完成99次整国交换及完整重搜索；总计300次搜索。上方表格展示原始最高分、随机最大值、超越次数及尾部比例，下面每个K均展示全部99次结果和图。所有设置相同，三种K交换映射逐一核查一致。
K=1原始最高分1.1981、3/99次随机达到或超过、尾部0.04；K=2原始1.9817、6/99、尾部0.07。K=3从先前3次流程检查扩大到99次，不覆盖旧试跑。
K=3理论L1上限2，浮点数可能略超过2，如2.0000000000000018。容差1e-12内视为并列，保留原始分数和未经容差处理的次数，不能把这种误差解释为超过随机分布。全体K=3联合有效6339条、810000个格子，99.23%格子为空，因此分数接近2往往缺乏区分度。完成99次不解决这一问题，也不证明跨国可交换假设成立。
本实验属于当前L1质量度量下的探索性随机参照，不是对每个subgroup都给出了正式有效的p值，不是Benford拟合检验，也不能据此判断数据造假。用户选择了整国交换方案，不能记录成Lucas或教授已正式认可。

K=3最终99次结果：原始最高L1=2.000000000000002；达到或超过原始（含容差并列）95/99；修正尾部比例=0.96。随机最高分范围1.999682337992376至2.000000000000002。运行耗时746.5秒；结束UTC时间2026-10-13T14:27:32.584729+00:00。原始最佳规则是北美洲与10.2 < 糖尿病患病率 ≤ 12.7667，48条有效记录、5个有效地区。图采用0至2.05的真实L1尺度，避免浮点级差异被自动缩放夸大。
K=3浮点并列核查——非常重要
最终99次中，95次与原始最高分相等（含1e-12绝对容差）或更高，尾部比例(95+1)/100=0.96。随机最高分范围约1.999682338至2，原始约2。因此K=3没有相对于本随机机制显得罕见。
如果对浮点数进行严格≥比较、不处理并列，只会得到5次和0.06；这主要由2附近的机器精度差异造成，不能当作合理的统计证据。本次原始值与严格比较结果仍保留在summary.json供核查，但解释必须使用有明确容差的0.96。
2026-10-13 16:27 CEST完成K=3搜索，耗时746.5秒，约12.4分钟。随后执行了三种K的全部99份映射、计数、尾部与试跑复现检查；12项单元测试通过。本笔记本所有代码单元均已执行且无错误输出。GitHub上传按用户最新指示暂停，本次未提交或推送任何文件。

9. 找到的subgroup到底是什么？成员与高分来源诊断
本节重新运行三次原始搜索以取得实际成员索引，断言最佳规则和分数与99次实验一致；没有重跑随机实验，没有调整筛选门槛。使用实际成员索引而非从显示文字重新解析区间，避免分箱边界误差。下面完整列出每个地区的有效周数、全部参与数字分布的具体周与值，以及差异最大的12个数字组合。
country_name来自本地OWID原始CSV的code→country映射，只用于可读名称，不改变分析数据。数字柱形图只展示L1贡献最大的12个组合；完整分布在all_occupied_digit_pairs.csv，不能把图中12个组合的差异之和当作全部L1。年度图数的是有效国家×周记录，不是感染人数或死亡人数。
eligibility_reasons是互斥原因分类：缺失优先，其次无穷、负数、零，再为正数但不足K位，最后有效。一行可能同时有零与缺失，按优先顺序只记一次；不能将该表误读为每个目标的独立缺失计数。这里观察的是Lucas预处理后的周值，零并不保证实际没有病例/死亡，可能受报告方式影响。

诊断结论——为什么要谨慎
K=1：5个地区合计1305条周记录，但只有22条同时有可统计的病例和死亡数字，约1.69%。1282条至少一列为零，1条至少一列缺失。Samoa贡献11条，即一半有效记录；其余为Tonga 5条、Marshall Islands 4条、Nauru和Tuvalu各1条。高分描述的是这22条记录的数字分布，不是整个五年完整疫情的稳定特征。随机尾部0.04仍需结合这一覆盖限制解释。
K=2：规则选中5个地区，但真正贡献21条有效记录的只有New Caledonia（7条）和French Polynesia（14条），另外Kiribati、Marshall Islands、Samoa没有有效记录。21条占1305条的1.61%，其中20条在2020–2021年，2022年1条、2023–2024年无有效记录。21条记录恰好落在21个不同数字组合里，分布非常稀疏。它与补集仍有20个共同组合，但共同概率质量只有约0.00917，所以L1约1.9817。不能把“很多共同格子”理解为频率接近。
K=3：48条有效记录落在48个不同数字组合；这些组合与补集没有任何重合，共同概率质量为0，所以L1在数值精度内等于2。这直接解释了分数饱和，不需要假设发现了特殊异常；99次参照尾部0.96也与此一致。
这些是搜索后描述性诊断，不是新增独立检验，不能证明差异完全由零/缺失导致，也不能推出数据造假或因果关系。本次不改变既定搜索或国家门槛。结果提示：目前发现主要由很少的有效周支撑，报告覆盖与数字位数限制是需要写进论文的核心限制。
本地诊断输出：本交付包根目录/outputs/best_subgroup_explanations_2026-10-13。JupyterLab：evaluation → outputs → best_subgroup_explanations_2026-10-13 → k1/k2/k3。all_subgroup_weeks.csv保留所有入选周；valid_subgroup_weeks.csv保留所有有效周。实现：evaluation → scripts → explain_best_subgroups.py。
