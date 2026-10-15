---
name: cn-etf-rotation-engine
description: 用户要比较已声明行业ETF观察池的相对强弱、核对轮动规则或测算历史调仓情景时使用；独立运行，不负责联网采集或交易。
metadata:
  version: 0.1.3
license: MIT
---

# ETF行业轮动

先确认观察池、指数身份、共同日历、价格口径和研究截止。首次使用及资料准备读 [BEGINNER.md](BEGINNER.md)。`cn-etf-rotation-engine review`计算相对强弱，`backtest`计算固定池历史情景；参数及旧规则见 [MIGRATION.md](MIGRATION.md)。

保留输入、方法版本、成本假设、来源缺口和新输出目录。没有历史成分/退市全集，不宣称历史池完整、全市场择优或无幸存者偏差。下一观察日收盘执行不称下一开盘成交。缺资料明确不能计算，不补价格、不把排名当概率，不执行交易。

本轮更新的 `composite` 用明确快照做四维研究评分，需要可选Node.js；缺少它仍可用Python的review/backtest，不切换到旧工作台算法。网页切换是临时情景，另存参数再生成新报告。`import-snapshots` 可整理使用者已有冻结日行情，不要求安装资料仓；先核对行业指数身份、原响应、同日历和分红拆分依据，不取交集掩盖缺日。输入与版本见 [USAGE.md](USAGE.md)。

## 安装与结果状态

本仓可以单独安装；pip安装命令行包不等于在助手中注册Skill。按本仓README安装完整资源，再使用SKILL中的入口。结果生成、资料取得与原文核验分别解释；未知说明影响及补齐路径。原创代码MIT，第三方代码保留许可，公告、研报和数据不随代码许可转移权利。
