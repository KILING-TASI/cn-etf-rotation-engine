# China ETF rotation research

A standalone standard-library tool for declared-pool relative momentum, legacy rotation rules, and fixed-pool historical scenarios. Acquisition belongs to cn-data-adapters; this tool neither fetches data nor trades.

Run `python try_demo.py --no-open --out-dir reports/demo`, or install with `python -m pip install .` and use `cn-etf-rotation-engine --help`. Skill registration is separate from CLI installation.

The teaching prices and calendar are fictional. Historical scenarios execute after signals at the next observed close, retain cost assumptions, and do not establish point-in-time universe completeness or future performance.

[Chinese overview](README.md) · [Detailed commands](USAGE.md) · [Input preparation](BEGINNER.md) · [Version history](CHANGELOG.md).
