const assert = require('assert');
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
  console.log('offline reading passed');

  // Sync test
  let called = false;
  global.fetch = (url, options) => {
    if (url.includes('/users/me/preferences')) {
      called = true;
      return Promise.resolve({ ok: true, json: async () => ({}) });
    }
    return Promise.reject(new Error('unknown url'));
  };
  await savePreferencesLocal({ effectsEnabled: true });
  await enqueue({ type: 'savePreferences', payload: { effectsEnabled: true } });
  const flushed = await flushQueue('token');
  const queue = await _getQueue();
  assert.strictEqual(flushed, 1);
  assert.strictEqual(queue.length, 0);
  assert.ok(called);
  console.log('sync passed');
})();
