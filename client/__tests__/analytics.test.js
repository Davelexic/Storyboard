const assert = require('assert');
const analytics = require('../services/analytics');

(async () => {
  let sent = null;
  global.fetch = async (url, opts) => {
    sent = JSON.parse(opts.body);
    return { ok: true, json: async () => ({ status: 'ok' }) };
  };

  analytics.logEvent('effect_toggle', { enabled: true });
  analytics.logEvent('chapter_complete', { chapter: 1 });
  assert.strictEqual(analytics._getQueue().length, 2);
  await analytics.flushEvents();
  assert.strictEqual(analytics._getQueue().length, 0);
  assert.ok(sent && sent.events.length === 2);
  // Test passed successfully
})();
