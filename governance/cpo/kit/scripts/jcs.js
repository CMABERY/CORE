#!/usr/bin/env node
/**
 * RFC 8785 JSON Canonicalization Scheme (JCS)
 *
 * - Rejects non-JSON numbers (NaN/Infinity).
 * - Canonicalizes -0 to 0.
 * - Sorts object keys by Unicode code point order (see note below).
 * - Uses JSON.stringify semantics for finite numbers.
 *
 * Usage:
 *   node scripts/jcs.js < input.json > canonical.json
 *   node scripts/jcs.js path/to/file.json
 */
'use strict';

const fs = require('fs');

function isPlainObject(x) {
  return x !== null && typeof x === 'object' && !Array.isArray(x);
}

function canonicalizeNumber(n) {
  if (typeof n !== 'number') throw new Error('Internal: not a number');
  if (!Number.isFinite(n)) {
    throw new Error('RFC8785: non-finite numbers (NaN/Infinity) are not permitted');
  }
  if (Object.is(n, -0)) return '0';
  return JSON.stringify(n);
}

// NOTE on key ordering:
// RFC8785 specifies ordering by Unicode code points.
// JavaScript's default string sort compares UTF-16 code units.
// This is deterministic and matches code point order for BMP keys.
// If you require strict code point ordering for astral symbols, implement
// a comparator over code points (rare in typical protocol keys).
function jcs(value) {
  if (value === null) return 'null';
  const t = typeof value;
  if (t === 'boolean') return value ? 'true' : 'false';
  if (t === 'number') return canonicalizeNumber(value);
  if (t === 'string') return JSON.stringify(value);

  if (Array.isArray(value)) {
    return '[' + value.map(v => jcs(v)).join(',') + ']';
  }

  if (isPlainObject(value)) {
    const keys = Object.keys(value).sort();
    let out = '{';
    for (let i = 0; i < keys.length; i++) {
      const k = keys[i];
      if (i) out += ',';
      out += JSON.stringify(k) + ':' + jcs(value[k]);
    }
    out += '}';
    return out;
  }

  throw new Error(`RFC8785: unsupported type in JSON data model: ${t}`);
}

function main() {
  const arg = process.argv[2];
  let input;
  if (arg) input = fs.readFileSync(arg, 'utf8');
  else input = fs.readFileSync(0, 'utf8');

  const value = JSON.parse(input);
  process.stdout.write(jcs(value));
}

if (require.main === module) {
  try {
    main();
  } catch (e) {
    console.error(String(e && e.message ? e.message : e));
    process.exit(1);
  }
}
