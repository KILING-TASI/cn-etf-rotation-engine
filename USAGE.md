# ETF行业轮动研究：详细使用说明

当前安装与教学入口见[首页](README.md)，资料准备见[BEGINNER](BEGINNER.md)。历史下载说明见[版本记录](CHANGELOG.md)。以下保留具体命令、方法、样本和限制，历史案例按各自日期阅读。

## 安装与自己的资料

```text
python -m pip install .
cn-etf-rotation-engine review --input 资料.json --out-dir reports/review
cn-etf-rotation-engine backtest --input 资料.json --out-dir reports/history
```

输入准备见 [BEGINNER.md](BEGINNER.md)，迁移与旧规则对应关系见 [MIGRATION.md](MIGRATION.md)。代码安装不自动注册Skill；作为Skill使用保留完整仓库资源。


## 结果的范围

相对动量不是预测，历史情景不是真实账户回测。观察池由使用者声明，未取得历史成分和退市全集，不能宣称全市场优选或没有幸存者偏差。信号在收盘后产生，下一观察日收盘执行；成本是统一基点假设。指数身份、复权、来源权利和真实交易日历需要另行核对。输出始终使用新目录。

[English](README.en.md) · [版本记录](CHANGELOG.md) · [验收范围](VALIDATION.md)


## 本轮更新：综合评分与冻结快照导入

```console
cn-etf-rotation-engine composite --input examples/composite-teaching.json --out-dir reports/composite
cn-etf-rotation-engine import-snapshots --input 明确冻结快照组合.json --out-dir reports/pool
cn-etf-rotation-engine review --input reports/pool/engine-input.json --out-dir reports/ranking
```

综合评分需要明确Node.js环境，缺少时提示安装途径，不自动安装；基础review/backtest仅Python。综合评分教学数据是虚构的，不是真实板块走势。新网页按原算法切换权重，另存情景参数后再次运行到新目录；旧报告不改。

导入要求2—100项同日历的cn-market-daily-archive/1.0成功快照及原JSON响应文本，逐项声明indexId、category=industry、comparability=declared-no-distribution-or-split、eventEvidence。未知事件不升级为无分红；不能把宽基/跨境ETF默认当行业ETF。
