import axios from 'axios';

const httpClient = axios.create({
    baseURL: 'http://localhost:5000',  // URL completa de la API
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    }
});

export default httpClient;