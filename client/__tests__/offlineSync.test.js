const assert = require('assert');
// Provide a minimal window.localStorage for AsyncStorage in Node
const store = {};
global.window = {
  localStorage: {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => {
      store[k] = v;
    },
    removeItem: (k) => {
      delete store[k];
    },
  },
};
const {
  saveBookMarkup,
  fetchBookMarkup,
  loadPreferencesLocal,
  savePreferencesLocal,
} = require('../utils/storage');
const { enqueue, flushQueue, _getQueue } = require('../utils/syncQueue');

(async () => {
  // Offline reading test
  await saveBookMarkup(1, { bookTitle: 'Cached', chapters: [{ text: 'Hello' }] });
  global.fetch = () => Promise.reject(new Error('network')); // simulate offline
  const data = await fetchBookMarkup(1, 'token');
  assert.strictEqual(data.bookTitle, 'Cached');
  // Offline reading test passed

  // Sync test
  let called = false;
  global.fetch = (url, options) => {
    if (url.includes('/users/me/preferences')) {
      called = true;
      return Promise.resolve({ ok: true, json: async () => ({}) });
    }
    return Promise.reject(new Error('unknown url'));
  };
  const prefs = {
    effectsEnabled: true,
    adaptiveBrightness: false,
    effects: { motion: { enabled: true, intensity: 0.5 } },
  };
  await savePreferencesLocal(prefs);
  const loaded = await loadPreferencesLocal();
  assert.deepStrictEqual(loaded, prefs);
  await enqueue({ type: 'savePreferences', payload: prefs });
  const flushed = await flushQueue('token');
  const queue = await _getQueue();
  assert.strictEqual(flushed, 1);
  assert.strictEqual(queue.length, 0);
  assert.ok(called);
  // Sync test passed
})();
