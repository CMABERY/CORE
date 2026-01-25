#!/usr/bin/env node
'use strict';

const assert = require('assert');
const { execSync } = require('child_process');
const path = require('path');

const jcsPath = path.join(__dirname, 'jcs.js');

function run(obj) {
  const input = JSON.stringify(obj);
  return execSync(`node "${jcsPath}"`, { input, encoding: 'utf8' });
}

(function testNegativeZero() {
  const out = run({ n: -0.0 });
  assert.strictEqual(out, '{"n":0}');
})();

(function testOrdering() {
  const out = run({ b: 1, a: 2 });
  assert.strictEqual(out, '{"a":2,"b":1}');
})();

console.log('OK: JCS basic tests passed.');
