const API_URL = 'http://127.0.0.1:8003';
const queue = [];
let flushing = false;

function logEvent(name, payload = {}) {
  queue.push({ name, payload, timestamp: Date.now() });
}

async function flushEvents() {
  if (flushing || queue.length === 0) return;
  flushing = true;
  const batch = queue.splice(0, queue.length);
  try {
    await fetch(`${API_URL}/analytics/events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ events: batch }),
    });
  } catch (err) {
    queue.unshift(...batch);
    console.error('Failed to upload analytics', err);
  } finally {
    flushing = false;
  }
}

const interval = setInterval(flushEvents, 5000);
if (interval.unref) interval.unref();

module.exports = {
  logEvent,
  flushEvents,
  _getQueue: () => queue,
};
module.exports.default = module.exports;
