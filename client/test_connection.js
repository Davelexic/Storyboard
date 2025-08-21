/**
 * Test script to verify client-server connection
 * Run this in the React Native environment to test API connectivity
 */

import apiClient from './services/api';
import authService from './services/auth';

/**
 * Test API connectivity
 */
export const testApiConnection = async () => {
  console.log('🔍 Testing API Connection...');
  
  try {
    // Test health check
    console.log('📋 Testing health check...');
    const health = await apiClient.healthCheck();
    console.log('✅ Health check passed:', health);
    
    // Test registration
    console.log('📋 Testing user registration...');
    const testEmail = `test${Date.now()}@example.com`;
    const testPassword = 'testpassword123';
    
    try {
      await apiClient.register(testEmail, testPassword);
      console.log('✅ Registration test passed');
    } catch (error) {
      if (error.message.includes('already exists')) {
        console.log('⚠️  User already exists (expected for repeated tests)');
      } else {
        throw error;
      }
    }
    
    // Test login
    console.log('📋 Testing user login...');
    const loginResult = await authService.login(testEmail, testPassword);
    console.log('✅ Login test passed:', loginResult.success);
    
    // Test getting user preferences
    console.log('📋 Testing user preferences...');
    const preferences = await apiClient.getUserPreferences();
    console.log('✅ User preferences test passed:', preferences);
    
    // Test getting books
    console.log('📋 Testing books endpoint...');
    const books = await apiClient.getBooks();
    console.log('✅ Books endpoint test passed:', books.length, 'books found');
    
    // Test logout
    console.log('📋 Testing logout...');
    await authService.logout();
    console.log('✅ Logout test passed');
    
    console.log('🎉 All API tests passed!');
    return true;
    
  } catch (error) {
    console.error('❌ API test failed:', error.message);
    return false;
  }
};

/**
 * Test specific endpoint
 */
export const testEndpoint = async (endpoint, method = 'GET', data = null) => {
  try {
    console.log(`🔍 Testing ${method} ${endpoint}...`);
    
    let response;
    switch (method.toUpperCase()) {
      case 'GET':
        response = await apiClient.request(endpoint);
        break;
      case 'POST':
        response = await apiClient.request(endpoint, {
          method: 'POST',
          body: data ? JSON.stringify(data) : null,
        });
        break;
      case 'PUT':
        response = await apiClient.request(endpoint, {
          method: 'PUT',
          body: data ? JSON.stringify(data) : null,
        });
        break;
      case 'DELETE':
        response = await apiClient.request(endpoint, {
          method: 'DELETE',
        });
        break;
      default:
        throw new Error(`Unsupported method: ${method}`);
    }
    
    console.log(`✅ ${method} ${endpoint} passed:`, response);
    return response;
    
  } catch (error) {
    console.error(`❌ ${method} ${endpoint} failed:`, error.message);
    throw error;
  }
};

export default {
  testApiConnection,
  testEndpoint,
};
