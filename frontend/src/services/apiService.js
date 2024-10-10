/* Interactions with the FastAPI backend */
import axios from 'axios';

const apiService = {
    sendQuery: (query) => {
        return axios.post('http://localhost:8000/query/', { user_input: query });
    }
};

export default apiService;
