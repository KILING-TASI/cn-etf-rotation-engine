---
name: cn-etf-rotation-engine
description: 用户要比较已声明行业ETF观察池的相对强弱、核对轮动规则或测算历史调仓情景时使用；独立运行，不负责联网采集或交易。
---

# ETF行业轮动

先确认观察池、指数身份、共同日历、价格口径和研究截止。首次使用及资料准备读 [BEGINNER.md](BEGINNER.md)。`cn-etf-rotation-engine review`计算相对强弱，`backtest`计算固定池历史情景；参数及旧规则见 [MIGRATION.md](MIGRATION.md)。

保留输入、方法版本、成本假设、来源缺口和新输出目录。没有历史成分/退市全集，不宣称历史池完整、全市场择优或无幸存者偏差。下一观察日收盘执行不称下一开盘成交。缺资料明确不能计算，不补价格、不把排名当概率，不执行交易。
