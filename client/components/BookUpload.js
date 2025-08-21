import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
  Modal,
  ProgressBarAndroid,
  Platform,
} from 'react-native';

export default function BookUpload({ onUpload, onClose, visible, token }) {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleUpload = async () => {
    setUploading(true);
    setUploadProgress(0);
    setUploadStatus('Preparing upload...');

    try {
      // In a real implementation, this would use react-native-document-picker
      // For now, we'll simulate the upload process
      
      // Simulate file selection
      setUploadStatus('Selecting file...');
      await new Promise(resolve => setTimeout(resolve, 1000));
      setUploadProgress(0.2);

      // Simulate file validation
      setUploadStatus('Validating EPUB file...');
      await new Promise(resolve => setTimeout(resolve, 1500));
      setUploadProgress(0.4);

      // Simulate upload
      setUploadStatus('Uploading to server...');
      await new Promise(resolve => setTimeout(resolve, 2000));
      setUploadProgress(0.7);

      // Simulate processing
      setUploadStatus('Processing book...');
      await new Promise(resolve => setTimeout(resolve, 1000));
      setUploadProgress(1.0);

      setUploadStatus('Upload complete!');
      
      // Show success message
      Alert.alert(
        'Upload Successful',
        'Your book has been uploaded and is being processed. You can check the status in your library.',
        [
          {
            text: 'OK',
            onPress: () => {
              setUploading(false);
              setUploadProgress(0);
              setUploadStatus('');
              onClose();
              if (onUpload) onUpload();
            }
          }
        ]
      );

    } catch (error) {
      setUploading(false);
      setUploadProgress(0);
      setUploadStatus('');
      
      Alert.alert(
        'Upload Error', 
        'Failed to upload book. Please check your connection and try again.',
        [
          {
            text: 'OK',
            onPress: () => onClose()
          }
        ]
      );
    }
  };

  const handleCancel = () => {
    if (uploading) {
      Alert.alert(
        'Cancel Upload',
        'Are you sure you want to cancel the upload?',
        [
          {
            text: 'Continue Upload',
            style: 'cancel'
          },
          {
            text: 'Cancel',
            style: 'destructive',
            onPress: () => {
              setUploading(false);
              setUploadProgress(0);
              setUploadStatus('');
              onClose();
            }
          }
        ]
      );
    } else {
      onClose();
    }
  };

  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="slide"
      onRequestClose={handleCancel}
    >
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          <Text style={styles.modalTitle}>Upload Book</Text>
          
          {!uploading ? (
            <>
              <Text style={styles.modalSubtitle}>
                Select an EPUB file to add to your library
              </Text>
              
              <View style={styles.buttonContainer}>
                <TouchableOpacity
                  style={[styles.button, styles.uploadButton]}
                  onPress={handleUpload}
                >
                  <Text style={styles.buttonText}>Choose EPUB File</Text>
                </TouchableOpacity>
                
                <TouchableOpacity
                  style={[styles.button, styles.cancelButton]}
                  onPress={handleCancel}
                >
                  <Text style={styles.cancelButtonText}>Cancel</Text>
                </TouchableOpacity>
              </View>
              
              <Text style={styles.helpText}>
                Supported formats: EPUB only{'\n'}
                Maximum file size: 50MB{'\n'}
                Processing time: 1-3 minutes
              </Text>
            </>
          ) : (
            <>
              <Text style={styles.modalSubtitle}>
                {uploadStatus}
              </Text>
              
              {/* Progress Bar */}
              <View style={styles.progressContainer}>
                {Platform.OS === 'android' ? (
                  <ProgressBarAndroid
                    styleAttr="Horizontal"
                    indeterminate={false}
                    progress={uploadProgress}
                    color="#3498db"
                  />
                ) : (
                  <View style={styles.progressBar}>
                    <View 
                      style={[
                        styles.progressFill, 
                        { width: `${uploadProgress * 100}%` }
                      ]} 
                    />
                  </View>
                )}
                <Text style={styles.progressText}>
                  {Math.round(uploadProgress * 100)}%
                </Text>
              </View>
              
              <View style={styles.buttonContainer}>
                <TouchableOpacity
                  style={[styles.button, styles.cancelButton]}
                  onPress={handleCancel}
                  disabled={uploading}
                >
                  <Text style={styles.cancelButtonText}>Cancel</Text>
                </TouchableOpacity>
              </View>
            </>
          )}
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 24,
    margin: 20,
    width: '90%',
    maxWidth: 400,
    alignItems: 'center',
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: 8,
  },
  modalSubtitle: {
    fontSize: 16,
    color: '#7f8c8d',
    textAlign: 'center',
    marginBottom: 24,
  },
  buttonContainer: {
    width: '100%',
    gap: 12,
  },
  button: {
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
    width: '100%',
  },
  uploadButton: {
    backgroundColor: '#3498db',
  },
  cancelButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#bdc3c7',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  cancelButtonText: {
    color: '#7f8c8d',
    fontSize: 16,
    fontWeight: '600',
  },
  helpText: {
    fontSize: 14,
    color: '#95a5a6',
    textAlign: 'center',
    marginTop: 16,
    lineHeight: 20,
  },
  progressContainer: {
    width: '100%',
    marginBottom: 24,
  },
  progressBar: {
    width: '100%',
    height: 8,
    backgroundColor: '#ecf0f1',
    borderRadius: 4,
    overflow: 'hidden',
    marginBottom: 8,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#3498db',
    borderRadius: 4,
  },
  progressText: {
    fontSize: 14,
    color: '#7f8c8d',
    textAlign: 'center',
  },
});
