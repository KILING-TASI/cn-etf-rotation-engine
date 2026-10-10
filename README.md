# ETF行业轮动研究

独立研究已声明ETF观察池的相对强弱、旧轮动规则和固定池历史调仓情景。只用Python标准库，不联网、不交易；数据采集归数据仓，持仓穿透归基金穿透仓，整体配置风险归组合引擎。

## 先试一次

```text
python try_demo.py --no-open --out-dir reports/first-demo
```

打开提示中的 `打开这里.html`。这是原创虚构资料，不是真实ETF表现或交易日历。Windows可运行Start-Demo.cmd，Linux/macOS可运行Start-Demo.sh。需要Python 3.10或以上，不需要其他作者仓库。

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

## 参与、更新与清理

[贡献说明](CONTRIBUTING.md) · [安全反馈](SECURITY.md) · [更新、缓存与卸载](LIFECYCLE.md)。
