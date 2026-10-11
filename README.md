# ETF行业轮动研究

研究声明ETF观察池的相对强弱、轮动规则与固定池历史调仓情景。

[![原创代码 MIT](https://img.shields.io/badge/原创代码-MIT-green)](LICENSE) · [当前发行版 v0.1.1](https://github.com/KILING-TASI/cn-etf-rotation-engine/releases/tag/v0.1.1) · [运行检查](https://github.com/KILING-TASI/cn-etf-rotation-engine/actions)

## 能解决什么问题

**观察池中的ETF谁更强？换规则和成本后，历史调仓结果怎样变化？**

轮动计算独立使用；数据采集归数据仓，持仓穿透归基金仓，整体配置风险归组合工具。

## 快速开始

从[发行页](https://github.com/KILING-TASI/cn-etf-rotation-engine/releases/tag/v0.1.1)下载完整源码并解压，需要 Python 3.10 或以上。在源码目录执行：

```text
python try_demo.py --no-open --out-dir reports/first-demo
```

按提示打开新生成的 HTML。Windows 也可双击 `Start-Demo.cmd`，Linux/macOS 可用 `sh Start-Demo.sh`。教学使用原创模拟资料，不自动取真实数据；重复运行使用新目录，历史结果保留。

## 使用自己的资料

先按[资料准备](BEGINNER.md)填写输入，再看[详细命令与方法](USAGE.md)。需要安装CLI时，在自己的Python环境运行：

```text
python -m pip install .
cn-etf-rotation-engine --help
```

仓库、Python发行包、安装命令及Skill注册名均为 `cn-etf-rotation-engine`。CLI安装和Skill注册是两个步骤：自然语言调用按[SKILL.md](SKILL.md)配置，保留完整资源；不必安装全部仓库。安装普通构建依赖可能联网，教学流程不需要作者缓存。

## 结果范围

相对动量不是预测；缺历史成分、退市全集和真实交易约束，不宣称全市场优选或完整账户回测。

报告中的来源、日期、假设和未知事项需一起阅读。程序运行成功不等于来源已经认证、资料完整或投资判断有效。原创代码采用MIT，第三方代码、公告、研报和数据仍按各自权利范围处理。

## 文档与维护

- [详细命令与方法](USAGE.md)
- [资料准备与排错](BEGINNER.md)
- [Skill调用指引](SKILL.md)
- [版本记录](CHANGELOG.md)
- [许可与第三方范围](THIRD_PARTY_NOTICES.md)
- [验收范围](VALIDATION.md)
- [旧规则迁移](MIGRATION.md)

[贡献说明](CONTRIBUTING.md) · [安全反馈](SECURITY.md) · [更新与清理](LIFECYCLE.md) · [English](README.en.md)

[按问题选择其他工具](https://github.com/KILING-TASI/research-workbench/blob/main/references/tool-navigation.md)。共12个活跃仓，资料契约校验已并入[数据仓](https://github.com/KILING-TASI/cn-data-adapters/blob/main/CONTRACT_MIGRATION.md)。各仓分别发布；main的后续文档整理不改写旧发行包和冻结结果。

## v0.1.1 本轮补强

独立综合评分、冻结行情导入、网页情景参数另存；不改旧结果。具体参数与边界见[使用说明](USAGE.md)。
