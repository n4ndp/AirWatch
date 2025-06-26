import httpClient from './api/httpClient';

const authService = {
    login: async (credentials) => {
        try {
            const response = await httpClient.post('/users/login', credentials);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.message || 'Login failed');
        }
    },

    register: async (userData) => {
        try {
            const response = await httpClient.post('/users/register', userData);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.message || 'Registration failed');
        }
    },

    logout: () => {
        sessionStorage.removeItem('token');
    }
};

export default authService;