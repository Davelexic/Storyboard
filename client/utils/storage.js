let AsyncStorage;
try {
  AsyncStorage = require('@react-native-async-storage/async-storage').default;
} catch (e) {
  const store = new Map();
  AsyncStorage = {
    async getItem(key) {
      return store.has(key) ? store.get(key) : null;
    },
    async setItem(key, value) {
      store.set(key, value);
    },
    async removeItem(key) {
      store.delete(key);
    },
  };
}

import API_CONFIG, { buildApiUrl } from '../config/api.js';

const API_URL = API_CONFIG.BASE_URL;

const BOOK_PREFIX = 'book_';
const PREFS_KEY = 'preferences';

async function saveBookMarkup(id, data) {
  await AsyncStorage.setItem(`${BOOK_PREFIX}${id}`, JSON.stringify(data));
}

async function loadBookMarkup(id) {
  const raw = await AsyncStorage.getItem(`${BOOK_PREFIX}${id}`);
  return raw ? JSON.parse(raw) : null;
}

async function fetchBookMarkup(id, token) {
  try {
    const res = await fetch(`${API_URL}/books/${id}/markup`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('Network error');
    const data = await res.json();
    await saveBookMarkup(id, data);
    return data;
  } catch (err) {
    const cached = await loadBookMarkup(id);
    if (cached) return cached;
    throw err;
  }
}

async function savePreferencesLocal(prefs) {
  await AsyncStorage.setItem(PREFS_KEY, JSON.stringify(prefs));
}

async function loadPreferencesLocal() {
  const raw = await AsyncStorage.getItem(PREFS_KEY);
  return raw ? JSON.parse(raw) : null;
}

module.exports = {
  storage: AsyncStorage,
  saveBookMarkup,
  loadBookMarkup,
  fetchBookMarkup,
  savePreferencesLocal,
  loadPreferencesLocal,
};
