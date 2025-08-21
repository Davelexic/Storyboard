import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  Modal,
} from 'react-native';

class NetworkErrorHandler extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isVisible: false,
      error: null,
      retryFunction: null,
    };
  }

  showError = (error, retryFunction = null) => {
    this.setState({
      isVisible: true,
      error,
      retryFunction,
    });
  };

  hideError = () => {
    this.setState({
      isVisible: false,
      error: null,
      retryFunction: null,
    });
  };

  handleRetry = () => {
    const { retryFunction } = this.state;
    
    if (retryFunction && typeof retryFunction === 'function') {
      this.hideError();
      retryFunction();
    } else {
      this.hideError();
    }
  };

  handleReportError = () => {
    const { error } = this.state;
    
    Alert.alert(
      'Report Network Error',
      'Would you like to report this network error?',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'Report',
          onPress: () => {
            // Here you would send the error to your error reporting service
            console.log('Reporting network error:', error);
            Alert.alert('Thank you', 'Network error has been reported.');
          },
        },
      ]
    );
  };

  getErrorMessage = (error) => {
    if (!error) return 'An unknown network error occurred.';
    
    // Handle different types of network errors
    if (error.status === 401) {
      return 'Authentication failed. Please log in again.';
    } else if (error.status === 403) {
      return 'Access denied. You don\'t have permission to perform this action.';
    } else if (error.status === 404) {
      return 'The requested resource was not found.';
    } else if (error.status === 429) {
      return 'Too many requests. Please wait a moment and try again.';
    } else if (error.status >= 500) {
      return 'Server error. Please try again later.';
    } else if (error.message === 'Network request failed') {
      return 'No internet connection. Please check your network and try again.';
    } else if (error.message === 'timeout') {
      return 'Request timed out. Please try again.';
    }
    
    return error.message || 'A network error occurred. Please try again.';
  };

  getErrorTitle = (error) => {
    if (!error) return 'Network Error';
    
    if (error.status === 401) {
      return 'Authentication Error';
    } else if (error.status === 403) {
      return 'Access Denied';
    } else if (error.status === 404) {
      return 'Not Found';
    } else if (error.status === 429) {
      return 'Rate Limited';
    } else if (error.status >= 500) {
      return 'Server Error';
    } else if (error.message === 'Network request failed') {
      return 'No Connection';
    } else if (error.message === 'timeout') {
      return 'Timeout';
    }
    
    return 'Network Error';
  };

  render() {
    const { isVisible, error } = this.state;
    const { children } = this.props;

    return (
      <>
        {children}
        
        <Modal
          visible={isVisible}
          transparent={true}
          animationType="fade"
          onRequestClose={this.hideError}
        >
          <View style={styles.modalOverlay}>
            <View style={styles.modalContent}>
              <Text style={styles.errorTitle}>
                {this.getErrorTitle(error)}
              </Text>
              
              <Text style={styles.errorMessage}>
                {this.getErrorMessage(error)}
              </Text>
              
              {__DEV__ && error && (
                <View style={styles.debugContainer}>
                  <Text style={styles.debugTitle}>Debug Information:</Text>
                  <Text style={styles.debugText}>
                    Status: {error.status || 'N/A'}
                  </Text>
                  <Text style={styles.debugText}>
                    URL: {error.url || 'N/A'}
                  </Text>
                  <Text style={styles.debugText}>
                    Method: {error.method || 'N/A'}
                  </Text>
                </View>
              )}
              
              <View style={styles.buttonContainer}>
                <TouchableOpacity
                  style={styles.retryButton}
                  onPress={this.handleRetry}
                >
                  <Text style={styles.retryButtonText}>Try Again</Text>
                </TouchableOpacity>
                
                <TouchableOpacity
                  style={styles.cancelButton}
                  onPress={this.hideError}
                >
                  <Text style={styles.cancelButtonText}>Cancel</Text>
                </TouchableOpacity>
                
                <TouchableOpacity
                  style={styles.reportButton}
                  onPress={this.handleReportError}
                >
                  <Text style={styles.reportButtonText}>Report</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        </Modal>
      </>
    );
  }
}

const styles = StyleSheet.create({
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalContent: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 24,
    width: '100%',
    maxWidth: 400,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.25,
    shadowRadius: 8,
    elevation: 5,
  },
  errorTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#e74c3c',
    textAlign: 'center',
    marginBottom: 12,
  },
  errorMessage: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 20,
  },
  debugContainer: {
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 16,
    marginBottom: 20,
  },
  debugTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#495057',
    marginBottom: 8,
  },
  debugText: {
    fontSize: 12,
    color: '#6c757d',
    fontFamily: 'monospace',
    lineHeight: 16,
    marginBottom: 4,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 8,
  },
  retryButton: {
    flex: 1,
    backgroundColor: '#3498db',
    borderRadius: 8,
    paddingVertical: 12,
    paddingHorizontal: 16,
    alignItems: 'center',
  },
  retryButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
  },
  cancelButton: {
    flex: 1,
    backgroundColor: '#95a5a6',
    borderRadius: 8,
    paddingVertical: 12,
    paddingHorizontal: 16,
    alignItems: 'center',
  },
  cancelButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
  },
  reportButton: {
    flex: 1,
    backgroundColor: '#e67e22',
    borderRadius: 8,
    paddingVertical: 12,
    paddingHorizontal: 16,
    alignItems: 'center',
  },
  reportButtonText: {
    color: 'white',
    fontSize: 14,
    fontWeight: '600',
  },
});

export default NetworkErrorHandler;
