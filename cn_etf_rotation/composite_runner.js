// SPDX-License-Identifier: MIT
const fs = require('fs');
const engine = require('./legacy/engine.js');
try {
  const spec = JSON.parse(fs.readFileSync(0, 'utf8'));
  const ranking = engine.calculate(spec.snapshot, spec.weights, spec.asOf);
  const funds = Object.fromEntries(Object.entries(spec.funds || {}).map(([key, rows]) => [key, engine.chooseFunds(rows, spec.asOf)]));
  const allocation = engine.allocate(ranking, spec.selected || []);
  process.stdout.write(JSON.stringify({ranking, funds, allocation, weights: spec.weights}));
} catch (error) { process.stderr.write(String(error.message)); process.exitCode = 2; }
