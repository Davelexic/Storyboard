const assert = require('assert');
const fs = require('fs');
const path = require('path');

const file = path.join(__dirname, '..', 'components', 'SettingsScreen.js');
const content = fs.readFileSync(file, 'utf8');

assert.ok(content.includes('Adaptive Brightness'), 'missing adaptive brightness toggle');
assert.ok(content.includes('effectsConfig'), 'missing per-effect configuration');
assert.ok(content.includes('intensity'), 'missing effect intensity slider');
console.log('settings screen ui passed');
