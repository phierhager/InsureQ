const API_URL = 'http://localhost:8000/api/data';

export const fetchData = async () => {
    const response = await fetch(API_URL);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};
