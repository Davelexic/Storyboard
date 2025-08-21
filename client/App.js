import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  Button,
  FlatList,
  TouchableOpacity,
  ScrollView,
  StyleSheet,
  SafeAreaView,
  StatusBar,
  Alert,
  ActivityIndicator,
  Dimensions,
  Animated,
} from 'react-native';
import SettingsScreen from './components/SettingsScreen';
import BookUpload from './components/BookUpload';

const API_URL = 'http://localhost:8000';
const { width, height } = Dimensions.get('window');

export default function App() {
  const [screen, setScreen] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState(null);
  const [books, setBooks] = useState([]);
  const [markup, setMarkup] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentChapter, setCurrentChapter] = useState(0);
  const [effectsEnabled, setEffectsEnabled] = useState(true);
  const [fontSize, setFontSize] = useState(16);
  const [brightness, setBrightness] = useState(1.0);
  const [effectIntensity, setEffectIntensity] = useState(0.5);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const fadeAnim = new Animated.Value(1);

  const loadPreferences = async () => {
    try {
      const res = await fetch(`${API_URL}/users/me/preferences`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const prefs = await res.json();
        setEffectsEnabled(prefs.effectsEnabled);
        setFontSize(prefs.fontSize);
        setBrightness(prefs.brightness);
        setEffectIntensity(prefs.effectIntensity);
      }
    } catch (err) {
      console.error('Failed to load preferences', err);
    }
  };

  const savePreferences = async () => {
    if (!token) return;
    const prefs = { effectsEnabled, fontSize, brightness, effectIntensity };
    try {
      await fetch(`${API_URL}/users/me/preferences`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(prefs),
      });
    } catch (err) {
      console.error('Failed to save preferences', err);
    }
  };

  useEffect(() => {
    if (token) {
      loadPreferences();
    }
  }, [token]);

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please enter both email and password');
      return;
    }
    
    setLoading(true);
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
      Alert.alert('Login Error', 'Invalid credentials. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please enter both email and password');
      return;
    }
    
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/users/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      if (!res.ok) throw new Error('Registration failed');
      Alert.alert('Success', 'Account created! Please login.');
    } catch (err) {
      Alert.alert('Registration Error', 'Failed to create account. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (screen === 'library' && token) {
      fetchBooks();
    }
  }, [screen, token]);

  const fetchBooks = async () => {
    try {
      const res = await fetch(`${API_URL}/books`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Failed to fetch books');
      const data = await res.json();
      setBooks(data);
    } catch (err) {
      Alert.alert('Error', 'Failed to load books');
      console.error(err);
    }
  };

  const openBook = async (id) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/books/${id}/markup`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Failed to load book');
      const data = await res.json();
      setMarkup(data);
      setCurrentChapter(0);
      setScreen('reader');
    } catch (err) {
      Alert.alert('Error', 'Failed to load book');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const renderEffect = (effect, text) => {
    if (!effectsEnabled) return text;

    switch (effect.type) {
      case 'text_style':
        return (
          <Text style={[styles.effectText, getEffectStyle(effect.style, effectIntensity)]}>
            {text}
          </Text>
        );
      case 'word_effect':
        if (effect.word && text.includes(effect.word)) {
          return (
            <Text style={[styles.effectText, getWordEffectStyle(effect.effect, effectIntensity)]}>
              {text}
            </Text>
          );
        }
        return text;
      case 'sound':
        // Audio effects would be implemented here
        return text;
      default:
        return text;
    }
  };

  const getEffectStyle = (style, intensity) => {
    const baseIntensity = intensity || 0.5;
    switch (style) {
      case 'fiery_sharp':
        return { 
          color: `rgba(255, 68, 68, ${baseIntensity})`, 
          fontWeight: 'bold',
          textShadowColor: 'rgba(255, 0, 0, 0.3)',
          textShadowOffset: { width: 1, height: 1 },
          textShadowRadius: 2
        };
      case 'calm_gentle':
        return { 
          color: `rgba(68, 136, 255, ${baseIntensity})`, 
          fontStyle: 'italic',
          textShadowColor: 'rgba(68, 136, 255, 0.2)',
          textShadowOffset: { width: 0, height: 1 },
          textShadowRadius: 1
        };
      default:
        return {};
    }
  };

  const getWordEffectStyle = (effect, intensity) => {
    const baseIntensity = intensity || 0.5;
    switch (effect) {
      case 'burn':
        return { 
          color: `rgba(255, 102, 0, ${baseIntensity})`, 
          fontWeight: 'bold',
          textShadowColor: 'rgba(255, 102, 0, 0.4)',
          textShadowOffset: { width: 1, height: 1 },
          textShadowRadius: 3
        };
      default:
        return {};
    }
  };

  const renderContent = (content) => {
    return content.map((item, index) => {
      const text = item.text || '';
      let displayText = text;

      if (item.effects && item.effects.length > 0) {
        displayText = item.effects.reduce((acc, effect) => 
          renderEffect(effect, acc), text);
      }

      return (
        <View key={index} style={styles.contentItem}>
          <Text style={[styles.contentText, { fontSize }]}>
            {displayText}
          </Text>
        </View>
      );
    });
  };

  const nextChapter = () => {
    if (markup && currentChapter < markup.chapters.length - 1) {
      Animated.sequence([
        Animated.timing(fadeAnim, { toValue: 0, duration: 200, useNativeDriver: true }),
        Animated.timing(fadeAnim, { toValue: 1, duration: 200, useNativeDriver: true })
      ]).start();
      setCurrentChapter(currentChapter + 1);
    }
  };

  const prevChapter = () => {
    if (currentChapter > 0) {
      Animated.sequence([
        Animated.timing(fadeAnim, { toValue: 0, duration: 200, useNativeDriver: true }),
        Animated.timing(fadeAnim, { toValue: 1, duration: 200, useNativeDriver: true })
      ]).start();
      setCurrentChapter(currentChapter - 1);
    }
  };

  const increaseFontSize = () => setFontSize(Math.min(fontSize + 2, 24));
  const decreaseFontSize = () => setFontSize(Math.max(fontSize - 2, 12));

  let content;
  if (screen === 'settings') {
    content = (
      <SettingsScreen
        onBack={() => setScreen('reader')}
        onSave={savePreferences}
        effectsEnabled={effectsEnabled}
        setEffectsEnabled={setEffectsEnabled}
        fontSize={fontSize}
        setFontSize={setFontSize}
        brightness={brightness}
        setBrightness={setBrightness}
        effectIntensity={effectIntensity}
        setEffectIntensity={setEffectIntensity}
      />
    );
  } else if (screen === 'login') {
    content = (
      <SafeAreaView style={styles.container}>
        <StatusBar barStyle="dark-content" />
        <View style={styles.loginContainer}>
          <Text style={styles.appTitle}>Cinei-read</Text>
          <Text style={styles.subtitle}>Where literature meets cinematic magic</Text>
          
          <View style={styles.formContainer}>
            <TextInput
              placeholder="Email"
              style={styles.input}
              value={email}
              onChangeText={setEmail}
              autoCapitalize="none"
              keyboardType="email-address"
            />
            <TextInput
              placeholder="Password"
              style={styles.input}
              value={password}
              onChangeText={setPassword}
              secureTextEntry
            />
            
            <View style={styles.buttonContainer}>
              <TouchableOpacity 
                style={[styles.button, styles.primaryButton]} 
                onPress={handleLogin}
                disabled={loading}
              >
                {loading ? (
                  <ActivityIndicator color="white" />
                ) : (
                  <Text style={styles.buttonText}>Login</Text>
                )}
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={[styles.button, styles.secondaryButton]} 
                onPress={handleRegister}
                disabled={loading}
              >
                <Text style={styles.secondaryButtonText}>Register</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </SafeAreaView>
    );
  } else if (screen === 'library') {
    content = (
      <SafeAreaView style={styles.container}>
        <StatusBar barStyle="dark-content" />
        <View style={styles.header}>
          <Text style={styles.title}>My Library</Text>
          <View style={styles.headerButtons}>
            <TouchableOpacity 
              style={styles.uploadButton}
              onPress={() => setShowUploadModal(true)}
            >
              <Text style={styles.uploadButtonText}>+ Add Book</Text>
            </TouchableOpacity>
            <TouchableOpacity 
              style={styles.logoutButton}
              onPress={() => {
                setToken(null);
                setScreen('login');
              }}
            >
              <Text style={styles.logoutText}>Logout</Text>
            </TouchableOpacity>
          </View>
        </View>
        
        {books.length === 0 ? (
          <View style={styles.emptyState}>
            <Text style={styles.emptyText}>No books in your library yet</Text>
            <Text style={styles.emptySubtext}>Upload a book to get started</Text>
          </View>
        ) : (
          <FlatList
            data={books}
            keyExtractor={(item) => String(item.id)}
            renderItem={({ item }) => (
              <TouchableOpacity
                style={styles.bookItem}
                onPress={() => openBook(item.id)}
              >
                <Text style={styles.bookTitle}>{item.title || `Book ${item.id}`}</Text>
                {item.author && <Text style={styles.bookAuthor}>{item.author}</Text>}
              </TouchableOpacity>
            )}
            style={styles.bookList}
          />
        )}
        
        {/* Book Upload Modal */}
        <BookUpload
          visible={showUploadModal}
          onClose={() => setShowUploadModal(false)}
          onUpload={() => {
            setShowUploadModal(false);
            fetchBooks(); // Refresh the book list
          }}
        />
      </SafeAreaView>
    );
  } else if (screen === 'reader') {
    const currentChapterData = markup?.chapters?.[currentChapter];
    
    content = (
      <SafeAreaView style={[styles.readerContainer, { backgroundColor: `rgba(255,255,255,${brightness})` }]}>
        <StatusBar barStyle="dark-content" />
        
        {/* Reader Header */}
        <View style={styles.readerHeader}>
          <TouchableOpacity onPress={() => setScreen('library')}>
            <Text style={styles.backButton}>← Library</Text>
          </TouchableOpacity>
          
          <Text style={styles.bookTitle} numberOfLines={1}>
            {markup?.bookTitle}
          </Text>
          
          <TouchableOpacity onPress={() => setScreen('settings')}>
            <Text style={styles.settingsButton}>⚙️</Text>
          </TouchableOpacity>
        </View>

        {/* Chapter Navigation */}
        <View style={styles.chapterNav}>
          <TouchableOpacity 
            onPress={prevChapter}
            disabled={currentChapter === 0}
            style={[styles.navButton, currentChapter === 0 && styles.navButtonDisabled]}
          >
            <Text style={styles.navButtonText}>← Previous</Text>
          </TouchableOpacity>
          
          <Text style={styles.chapterInfo}>
            Chapter {currentChapter + 1} of {markup?.chapters?.length}
          </Text>
          
          <TouchableOpacity 
            onPress={nextChapter}
            disabled={!markup || currentChapter >= markup.chapters.length - 1}
            style={[styles.navButton, (!markup || currentChapter >= markup.chapters.length - 1) && styles.navButtonDisabled]}
          >
            <Text style={styles.navButtonText}>Next →</Text>
          </TouchableOpacity>
        </View>

        {/* Reading Content */}
        <Animated.View style={[styles.readerContent, { opacity: fadeAnim }]}>
          <ScrollView 
            style={styles.scrollView}
            showsVerticalScrollIndicator={false}
            contentContainerStyle={styles.scrollContent}
          >
            {currentChapterData?.chapterTitle && (
              <Text style={[styles.chapterTitle, { fontSize: fontSize + 4 }]}>
                {currentChapterData.chapterTitle}
              </Text>
            )}
            
            {currentChapterData?.content && renderContent(currentChapterData.content)}
          </ScrollView>
        </Animated.View>

        {/* Quick Controls */}
        <View style={styles.quickControls}>
          <TouchableOpacity onPress={decreaseFontSize} style={styles.controlButton}>
            <Text style={styles.controlText}>A-</Text>
          </TouchableOpacity>
          
          <TouchableOpacity onPress={increaseFontSize} style={styles.controlButton}>
            <Text style={styles.controlText}>A+</Text>
          </TouchableOpacity>
          
          <TouchableOpacity 
            onPress={() => setEffectsEnabled(!effectsEnabled)} 
            style={[styles.controlButton, !effectsEnabled && styles.controlButtonDisabled]}
          >
            <Text style={styles.controlText}>{effectsEnabled ? '✨' : '⚪'}</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return content;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  loginContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  appTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#7f8c8d',
    marginBottom: 40,
    textAlign: 'center',
  },
  formContainer: {
    width: '100%',
    maxWidth: 300,
  },
  input: {
    width: '100%',
    padding: 15,
    marginBottom: 15,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    fontSize: 16,
    backgroundColor: 'white',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 10,
  },
  button: {
    flex: 1,
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
  },
  primaryButton: {
    backgroundColor: '#3498db',
  },
  secondaryButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#3498db',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  secondaryButtonText: {
    color: '#3498db',
    fontSize: 16,
    fontWeight: '600',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
    backgroundColor: 'white',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  headerButtons: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  uploadButton: {
    padding: 8,
    backgroundColor: '#27ae60',
    borderRadius: 6,
  },
  uploadButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
  },
  logoutButton: {
    padding: 8,
  },
  logoutText: {
    color: '#e74c3c',
    fontSize: 16,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  emptyText: {
    fontSize: 18,
    color: '#7f8c8d',
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#bdc3c7',
    textAlign: 'center',
  },
  bookList: {
    flex: 1,
  },
  bookItem: {
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
    backgroundColor: 'white',
  },
  bookTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: 4,
  },
  bookAuthor: {
    fontSize: 14,
    color: '#7f8c8d',
  },
  readerContainer: {
    flex: 1,
    backgroundColor: '#fefefe',
  },
  readerHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
    backgroundColor: 'white',
  },
  backButton: {
    fontSize: 16,
    color: '#3498db',
    fontWeight: '600',
  },
  settingsButton: {
    fontSize: 20,
  },
  chapterNav: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 15,
    backgroundColor: '#f8f9fa',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  navButton: {
    padding: 10,
    borderRadius: 6,
    backgroundColor: '#3498db',
  },
  navButtonDisabled: {
    backgroundColor: '#bdc3c7',
  },
  navButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
  },
  chapterInfo: {
    fontSize: 14,
    color: '#7f8c8d',
    fontWeight: '500',
  },
  readerContent: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
  },
  chapterTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 20,
    textAlign: 'center',
  },
  contentItem: {
    marginBottom: 16,
  },
  contentText: {
    fontSize: 16,
    lineHeight: 24,
    color: '#2c3e50',
    textAlign: 'justify',
  },
  effectText: {
    // Base effect styling
  },
  quickControls: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 15,
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  controlButton: {
    padding: 12,
    borderRadius: 8,
    backgroundColor: '#f8f9fa',
    minWidth: 50,
    alignItems: 'center',
  },
  controlButtonDisabled: {
    backgroundColor: '#e9ecef',
  },
  controlText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2c3e50',
  },
});

