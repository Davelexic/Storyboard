/**
 * API Service for Cinematic Reading Engine
 * Handles all communication with the backend API
 */

// Configuration
const API_CONFIG = {
  BASE_URL: 'http://127.0.0.1:8003', // Updated to match our backend
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
};

// API endpoints
const ENDPOINTS = {
  // Authentication
  LOGIN: '/users/login',
  REGISTER: '/users/register',
  
  // Users
  USERS: '/users/',
  USER_PREFERENCES: '/users/me/preferences',
  
  // Books
  BOOKS: '/books/',
  BOOK_UPLOAD: '/books/upload',
  BOOK_JOB_STATUS: '/books/jobs/{job_id}/status',
  BOOK_JOB_RESULT: '/books/jobs/{job_id}/result',
  BOOK_MARKUP: '/books/{book_id}/markup',
  
  // Analytics
  ANALYTICS_EVENTS: '/analytics/events',
  
  // Health
  HEALTH: '/',
};

/**
 * API Client class
 */
class ApiClient {
  constructor() {
    this.baseURL = API_CONFIG.BASE_URL;
    this.token = null;
  }

  /**
   * Set authentication token
   */
  setToken(token) {
    this.token = token;
  }

  /**
   * Clear authentication token
   */
  clearToken() {
    this.token = null;
  }

  /**
   * Get headers for API requests
   */
  getHeaders(contentType = 'application/json') {
    const headers = {
      'Content-Type': contentType,
    };
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    return headers;
  }

  /**
   * Make API request with error handling and retries
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getHeaders(),
      timeout: API_CONFIG.TIMEOUT,
      ...options,
    };

    // Handle multipart/form-data
    if (options.body instanceof FormData) {
      delete config.headers['Content-Type'];
    }

    let lastError;
    
    for (let attempt = 1; attempt <= API_CONFIG.RETRY_ATTEMPTS; attempt++) {
      try {
        const response = await fetch(url, config);
        
        // Handle successful responses
        if (response.ok) {
          const contentType = response.headers.get('content-type');
          if (contentType && contentType.includes('application/json')) {
            return await response.json();
          }
          return await response.text();
        }
        
        // Handle error responses
        if (response.status === 401) {
          this.clearToken();
          throw new Error('Authentication failed');
        }
        
        if (response.status === 422) {
          const errorData = await response.json();
          throw new Error(`Validation error: ${JSON.stringify(errorData.detail)}`);
        }
        
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        
      } catch (error) {
        lastError = error;
        
        if (attempt === API_CONFIG.RETRY_ATTEMPTS) {
          throw error;
        }
        
        // Wait before retry (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
      }
    }
    
    throw lastError;
  }

  // Authentication methods
  async login(email, password) {
    const response = await this.request(ENDPOINTS.LOGIN, {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    
    this.setToken(response.access_token);
    return response;
  }

  async register(email, password) {
    return await this.request(ENDPOINTS.REGISTER, {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  // User methods
  async getUsers() {
    return await this.request(ENDPOINTS.USERS);
  }

  async getUser(userId) {
    return await this.request(ENDPOINTS.USERS + userId);
  }

  async getUserPreferences() {
    return await this.request(ENDPOINTS.USER_PREFERENCES);
  }

  async updateUserPreferences(preferences) {
    return await this.request(ENDPOINTS.USER_PREFERENCES, {
      method: 'PUT',
      body: JSON.stringify(preferences),
    });
  }

  // Book methods
  async getBooks() {
    return await this.request(ENDPOINTS.BOOKS);
  }

  async getBook(bookId) {
    return await this.request(ENDPOINTS.BOOKS + bookId);
  }

  async deleteBook(bookId) {
    return await this.request(ENDPOINTS.BOOKS + bookId, {
      method: 'DELETE',
    });
  }

  async uploadBook(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    return await this.request(ENDPOINTS.BOOK_UPLOAD, {
      method: 'POST',
      body: formData,
    });
  }

  async getJobStatus(jobId) {
    return await this.request(ENDPOINTS.BOOK_JOB_STATUS.replace('{job_id}', jobId));
  }

  async getJobResult(jobId) {
    return await this.request(ENDPOINTS.BOOK_JOB_RESULT.replace('{job_id}', jobId));
  }

  async getBookMarkup(bookId) {
    return await this.request(ENDPOINTS.BOOK_MARKUP.replace('{book_id}', bookId));
  }

  // Analytics methods
  async getAnalyticsEvents() {
    return await this.request(ENDPOINTS.ANALYTICS_EVENTS);
  }

  async postAnalyticsEvents(events) {
    return await this.request(ENDPOINTS.ANALYTICS_EVENTS, {
      method: 'POST',
      body: JSON.stringify({ events }),
    });
  }

  // Health check
  async healthCheck() {
    return await this.request(ENDPOINTS.HEALTH);
  }
}

// Create and export singleton instance
const apiClient = new ApiClient();

export default apiClient;
export { ENDPOINTS, API_CONFIG };
