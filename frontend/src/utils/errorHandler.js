// Comprehensive error handling utilities
export class ErrorHandler {
  // Handle API errors
  static handleApiError(error, defaultMessage = 'An unexpected error occurred') {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;

      switch (status) {
        case 400:
          return {
            message: data.detail || 'Bad request',
            severity: 'error',
            code: 'BAD_REQUEST'
          };
        case 401:
          return {
            message: data.detail || 'Unauthorized. Please log in again.',
            severity: 'warning',
            code: 'UNAUTHORIZED'
          };
        case 403:
          return {
            message: data.detail || 'Access forbidden',
            severity: 'error',
            code: 'FORBIDDEN'
          };
        case 404:
          return {
            message: data.detail || 'Resource not found',
            severity: 'error',
            code: 'NOT_FOUND'
          };
        case 422:
          return {
            message: data.detail || 'Validation error',
            severity: 'error',
            code: 'VALIDATION_ERROR'
          };
        case 500:
          return {
            message: data.detail || 'Internal server error',
            severity: 'error',
            code: 'INTERNAL_ERROR'
          };
        default:
          return {
            message: data.detail || `Server error (${status})`,
            severity: 'error',
            code: 'SERVER_ERROR'
          };
      }
    } else if (error.request) {
      // Request was made but no response received
      return {
        message: 'Network error. Please check your connection.',
        severity: 'warning',
        code: 'NETWORK_ERROR'
      };
    } else {
      // Something else happened
      return {
        message: error.message || defaultMessage,
        severity: 'error',
        code: 'CLIENT_ERROR'
      };
    }
  }

  // Show user-friendly error messages
  static showErrorNotification(errorInfo, customMessage = null) {
    const message = customMessage || errorInfo.message;

    // Create a notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-md shadow-lg z-50 max-w-sm ${
      errorInfo.severity === 'warning'
        ? 'bg-yellow-100 border border-yellow-400 text-yellow-700'
        : 'bg-red-100 border border-red-400 text-red-700'
    }`;

    notification.innerHTML = `
      <div class="flex items-start">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 ${errorInfo.severity === 'warning' ? 'text-yellow-400' : 'text-red-400'}" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium">${errorInfo.code}</h3>
          <div class="mt-2 text-sm">${message}</div>
        </div>
        <button class="ml-auto flex-shrink-0 text-gray-400 hover:text-gray-500" onclick="this.parentElement.parentElement.remove()">
          <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    `;

    document.body.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
      if (notification.parentNode) {
        notification.remove();
      }
    }, 5000);
  }

  // Log errors for debugging
  static logError(error, context = '') {
    console.error(`[${new Date().toISOString()}] ${context}`, {
      message: error.message,
      stack: error.stack,
      ...(error.response && { response: error.response }),
      ...(error.request && { request: error.request })
    });
  }

  // Validate form inputs
  static validateInputs(formData, rules) {
    const errors = {};

    for (const [field, value] of Object.entries(formData)) {
      if (rules[field]) {
        for (const rule of rules[field]) {
          const result = rule(value);
          if (!result.valid) {
            errors[field] = result.message;
            break;
          }
        }
      }
    }

    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  }
}

// Validation rules
export const validationRules = {
  email: [
    (value) => ({
      valid: !!value,
      message: 'Email is required'
    }),
    (value) => ({
      valid: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
      message: 'Please enter a valid email address'
    })
  ],
  password: [
    (value) => ({
      valid: !!value,
      message: 'Password is required'
    }),
    (value) => ({
      valid: value.length >= 8,
      message: 'Password must be at least 8 characters long'
    }),
    (value) => ({
      valid: /[A-Z]/.test(value) && /[a-z]/.test(value) && /\d/.test(value),
      message: 'Password must contain uppercase, lowercase, and numeric characters'
    })
  ],
  username: [
    (value) => ({
      valid: !!value,
      message: 'Username is required'
    }),
    (value) => ({
      valid: value.length >= 3 && value.length <= 30,
      message: 'Username must be between 3 and 30 characters'
    }),
    (value) => ({
      valid: /^[a-zA-Z0-9_-]+$/.test(value),
      message: 'Username can only contain letters, numbers, underscores, and hyphens'
    })
  ],
  title: [
    (value) => ({
      valid: !!value,
      message: 'Title is required'
    }),
    (value) => ({
      valid: value.length >= 1 && value.length <= 200,
      message: 'Title must be between 1 and 200 characters'
    })
  ],
  description: [
    (value) => ({
      valid: !value || value.length <= 1000,
      message: 'Description must be 1000 characters or less'
    })
  ]
};

// Error boundary component for React
export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });

    // Log the error
    ErrorHandler.logError(error, 'React Error Boundary');
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
          <div className="max-w-md w-full bg-white rounded-lg shadow-md p-6">
            <div className="text-center">
              <svg className="mx-auto h-12 w-12 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">Something went wrong</h3>
              <p className="mt-1 text-sm text-gray-500">
                An error occurred while loading this component.
              </p>
              <div className="mt-6">
                <button
                  type="button"
                  onClick={() => window.location.reload()}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Refresh page
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}