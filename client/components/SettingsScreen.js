import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  StatusBar,
  Switch,
  Slider,
} from 'react-native';

export default function SettingsScreen({
  onBack,
  onSave,
  effectsEnabled,
  setEffectsEnabled,
  fontSize,
  setFontSize,
  brightness,
  setBrightness,
  effectIntensity,
  setEffectIntensity
}) {
  const handleBack = () => {
    if (onSave) {
      onSave();
    }
    onBack();
  };
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={handleBack}>
          <Text style={styles.backButton}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.title}>Settings</Text>
        <View style={{ width: 50 }} />
      </View>

      {/* Settings Content */}
      <View style={styles.content}>
        {/* Reading Experience */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Reading Experience</Text>
          
          {/* Font Size */}
          <View style={styles.settingItem}>
            <Text style={styles.settingLabel}>Font Size: {fontSize}px</Text>
            <Slider
              style={styles.slider}
              minimumValue={12}
              maximumValue={24}
              value={fontSize}
              onValueChange={setFontSize}
              minimumTrackTintColor="#3498db"
              maximumTrackTintColor="#bdc3c7"
              thumbStyle={styles.sliderThumb}
            />
          </View>

          {/* Brightness */}
          <View style={styles.settingItem}>
            <Text style={styles.settingLabel}>Brightness: {Math.round(brightness * 100)}%</Text>
            <Slider
              style={styles.slider}
              minimumValue={0.3}
              maximumValue={1.0}
              value={brightness}
              onValueChange={setBrightness}
              minimumTrackTintColor="#3498db"
              maximumTrackTintColor="#bdc3c7"
              thumbStyle={styles.sliderThumb}
            />
          </View>
        </View>

        {/* Effects */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Cinematic Effects</Text>
          
          {/* Enable Effects */}
          <View style={styles.settingItem}>
            <Text style={styles.settingLabel}>Enable Effects</Text>
            <Switch
              value={effectsEnabled}
              onValueChange={setEffectsEnabled}
              trackColor={{ false: '#bdc3c7', true: '#3498db' }}
              thumbColor={effectsEnabled ? '#ffffff' : '#f4f3f4'}
            />
          </View>

          {/* Effect Intensity */}
          {effectsEnabled && (
            <View style={styles.settingItem}>
              <Text style={styles.settingLabel}>Effect Intensity: {Math.round(effectIntensity * 100)}%</Text>
              <Slider
                style={styles.slider}
                minimumValue={0.1}
                maximumValue={1.0}
                value={effectIntensity}
                onValueChange={setEffectIntensity}
                minimumTrackTintColor="#3498db"
                maximumTrackTintColor="#bdc3c7"
                thumbStyle={styles.sliderThumb}
              />
            </View>
          )}
        </View>

        {/* About */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>About</Text>
          <View style={styles.aboutItem}>
            <Text style={styles.aboutLabel}>Version</Text>
            <Text style={styles.aboutValue}>1.0.0</Text>
          </View>
          <View style={styles.aboutItem}>
            <Text style={styles.aboutLabel}>Build</Text>
            <Text style={styles.aboutValue}>2024.1.15</Text>
          </View>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
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
  backButton: {
    fontSize: 16,
    color: '#3498db',
    fontWeight: '600',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2c3e50',
  },
  content: {
    flex: 1,
    padding: 20,
  },
  section: {
    marginBottom: 30,
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 15,
  },
  settingItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  settingLabel: {
    fontSize: 16,
    color: '#2c3e50',
    flex: 1,
  },
  slider: {
    flex: 1,
    marginLeft: 20,
  },
  sliderThumb: {
    backgroundColor: '#3498db',
  },
  aboutItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  aboutLabel: {
    fontSize: 16,
    color: '#7f8c8d',
  },
  aboutValue: {
    fontSize: 16,
    color: '#2c3e50',
    fontWeight: '500',
  },
});
