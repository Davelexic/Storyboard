import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, FlatList, TouchableOpacity, ScrollView, StyleSheet } from 'react-native';

const API_URL = 'http://localhost:8000';

export default function App() {
  const [screen, setScreen] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState(null);
  const [books, setBooks] = useState([]);
  const [markup, setMarkup] = useState(null);

  const handleLogin = async () => {
    try {
      const res = await fetch(`${API_URL}/users/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      if (!res.ok) throw new Error('Login failed');
      const data = await res.json();
      setToken(data.access_token);
      setScreen('library');
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    if (screen === 'library' && token) {
      fetch(`${API_URL}/books`, {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then((res) => res.json())
        .then(setBooks)
        .catch(console.error);
    }
  }, [screen, token]);

  const openBook = async (id) => {
    try {
      const res = await fetch(`${API_URL}/books/${id}/markup`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Failed to load book');
      const data = await res.json();
      setMarkup(data);
      setScreen('reader');
    } catch (err) {
      console.error(err);
    }
  };

  let content;
  if (screen === 'login') {
    content = (
      <View style={styles.container}>
        <Text style={styles.title}>Login</Text>
        <TextInput
          placeholder="Email"
          style={styles.input}
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
        />
        <TextInput
          placeholder="Password"
          style={styles.input}
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        <Button title="Login" onPress={handleLogin} />
      </View>
    );
  } else if (screen === 'library') {
    content = (
      <View style={styles.container}>
        <Text style={styles.title}>My Library</Text>
        <FlatList
          data={books}
          keyExtractor={(item) => String(item.id)}
          renderItem={({ item }) => (
            <TouchableOpacity
              style={styles.bookItem}
              onPress={() => openBook(item.id)}
            >
              <Text>{item.title || `Book ${item.id}`}</Text>
            </TouchableOpacity>
          )}
        />
      </View>
    );
  } else if (screen === 'reader') {
    content = (
      <ScrollView contentContainerStyle={styles.container}>
        <Button title="Back" onPress={() => setScreen('library')} />
        <Text style={styles.markup}>{JSON.stringify(markup, null, 2)}</Text>
      </ScrollView>
    );
  }

  return content;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    alignItems: 'center',
    justifyContent: 'center'
  },
  title: {
    fontSize: 20,
    marginBottom: 16
  },
  input: {
    width: '80%',
    padding: 8,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 4
  },
  bookItem: {
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
    width: '100%'
  },
  markup: {
    marginTop: 16
  }
});

