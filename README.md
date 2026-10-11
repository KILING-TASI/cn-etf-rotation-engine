# ETF行业轮动研究

研究声明ETF观察池的相对强弱、轮动规则与固定池历史调仓情景。

[原创代码 MIT](LICENSE) · [发行说明](https://github.com/KILING-TASI/cn-etf-rotation-engine/releases/tag/v0.1.2) · [运行检查](https://github.com/KILING-TASI/cn-etf-rotation-engine/actions) · [English](README.en.md)

当前发布：**v0.1.2 · 普通发行版**。Python **3.10+**；基础功能只需 Python，无第三方运行依赖。

[快速开始](#快速开始) · [使用自己的资料](#使用自己的资料) · [能力与边界](#能力与边界) · [文档与维护](#文档与维护)

## 能解决什么问题

**观察池中的ETF谁更强？换规则和成本后，历史调仓结果怎样变化？**

轮动计算独立使用；数据采集归数据仓，持仓穿透归基金仓，整体配置风险归组合工具。

| 需要准备 | 会得到什么 |
|---|---|
| 明确的 ETF 观察池、历史价格、交易日与成本假设。 | 相对强弱评分、声明规则下的固定池历史调仓与成本记录。 |

## 快速开始

1. 安装 Python 3.10 或以上版本。
2. 下载[完整源码 ZIP](https://github.com/KILING-TASI/cn-etf-rotation-engine/releases/download/v0.1.2/cn-etf-rotation-engine-v0.1.2-source.zip)并解压，进入包含 `try_demo.py` 的目录。
3. 在该目录打开终端，运行：

```console
python try_demo.py --no-open --out-dir reports/first-demo
```

按终端给出的路径打开 HTML。也可以在源码目录双击 `Start-Demo.cmd`（Windows），或运行 `sh Start-Demo.sh`（Linux/macOS）。教学使用原创模拟资料，不自动取得真实数据。

使用 Git 时，先运行 `git clone https://github.com/KILING-TASI/cn-etf-rotation-engine.git`，再运行 `cd cn-etf-rotation-engine`，随后执行上面的教学命令。重复运行请指定新目录，历史结果会保留。

## 使用自己的资料

先按[资料准备与排错](BEGINNER.md)整理来源、日期、单位和必要字段，再按[使用说明](USAGE.md)选择对应入口。以下两种使用方式分别配置。

**命令行（CLI）**：在源码目录安装本仓，然后查看可用命令：

```console
python -m pip install .
cn-etf-rotation-engine --help
```

基础安装不需要科学计算或 PDF 组件。安装时下载构建工具或可选依赖可能需要联网。

**助手 Skill**：按 [SKILL.md](SKILL.md) 配置，保留完整目录及其引用资源。安装 CLI 不会自动注册 Skill，也不表示已在第三方技能市场上架。

| 身份 | 名称 |
|---|---|
| GitHub 仓库 / Python 发行包 | `cn-etf-rotation-engine` |
| 主要命令 | `cn-etf-rotation-engine` |
| SKILL.md 中的名称 | `cn-etf-rotation-engine` |

本仓可单独使用。需要跨工具功能时，再按说明安装并明确配置对应工具的位置。

## 能力与边界

相对动量不是预测；缺历史成分、退市全集和真实交易约束，不宣称全市场优选或完整账户回测。

报告中的来源、日期、假设和未知事项需一起阅读。程序运行成功不等于来源已经认证、资料完整或投资判断有效。原创代码采用MIT，第三方代码、公告、研报和数据仍按各自权利范围处理。

## 文档与维护

- [详细命令与方法](USAGE.md)
- [资料准备与排错](BEGINNER.md)
- [Skill 调用指引](SKILL.md)
- [版本记录](CHANGELOG.md)
- [许可与第三方范围](THIRD_PARTY_NOTICES.md)
- [验收范围](VALIDATION.md)
- [旧规则迁移](MIGRATION.md)

[贡献说明](CONTRIBUTING.md) · [安全反馈](SECURITY.md) · [更新与清理](LIFECYCLE.md)

[按问题选择其他工具](https://github.com/KILING-TASI/research-workbench/blob/main/references/tool-navigation.md)；资料契约校验已并入[数据仓](https://github.com/KILING-TASI/cn-data-adapters/blob/main/CONTRACT_MIGRATION.md)。默认分支的文档整理不改写已发布的源码包和历史结果；版本变化见 [CHANGELOG.md](CHANGELOG.md)。
