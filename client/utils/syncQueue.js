const { storage } = require('./storage');

const QUEUE_KEY = 'syncQueue';
const API_URL = 'http://localhost:8000';

async function getQueue() {
  const raw = await storage.getItem(QUEUE_KEY);
  return raw ? JSON.parse(raw) : [];
}

async function setQueue(queue) {
  if (!queue.length) {
    await storage.removeItem(QUEUE_KEY);
  } else {
    await storage.setItem(QUEUE_KEY, JSON.stringify(queue));
  }
}

async function enqueue(action) {
  const queue = await getQueue();
  queue.push(action);
  await setQueue(queue);
}

async function flushQueue(token) {
  const queue = await getQueue();
  const remaining = [];
  for (const action of queue) {
    try {
      if (action.type === 'savePreferences') {
        await fetch(`${API_URL}/users/me/preferences`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(action.payload),
        });
      }
    } catch (err) {
      remaining.push(action);
    }
  }
  await setQueue(remaining);
  return queue.length - remaining.length;
}

module.exports = {
  enqueue,
  flushQueue,
  _getQueue: getQueue, // for testing
};
