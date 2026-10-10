# 准备ETF研究资料

先用教学结果了解输出。真实资料的origin填写declared-history，asOf为研究截止日，dates为唯一升序共同日期，rows为已声明观察池；每行明确symbol、index、type=industry、eligible=true、closes。各行价格数量与dates相同，全部是正有限数值。两个ETF不能重复代表同一指数来凑排名。

marketCloses可选；没有时不应用旧市场风险档位，明确保留限制。topN、rebalanceEvery、costBps为历史情景参数；不把统一基点成本当成实际交易收费。价格复权方式、分红、币种、身份与来源须由资料提供者核对，现有输入不是自动核验的证券名录。

未通过时先核对身份、日期、缺值和输出目录，不能填零凑齐。结果含input.json、result.json、打开这里.html及文件摘要。更新资料使用新目录，不改冻结历史。

真实资料须在顶层明确currency=CNY和priceBasis（provided-price或provided-total-return），每行明确market=SSE或SZSE；不能隐式换汇。价格收益口径不包含未提供的分红现金，不能当成完整总回报。
