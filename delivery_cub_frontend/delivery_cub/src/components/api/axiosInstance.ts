import axios, { AxiosInstance } from 'axios';
import { refreshAccessToken } from './auth';

export const BASE_URL = 'http://127.0.0.1:8000/';

const axiosInstance: AxiosInstance = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});


axiosInstance.interceptors.request.use((config: any) => {
    const accessToken = sessionStorage.getItem('accessToken');
    if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
}, (error: any) => {
    return Promise.reject(error);
});


axiosInstance.interceptors.response.use(
    (response: any) => response,
    async (error: { config: any; response: { status: number; }; }) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            const newAccessToken = await refreshAccessToken(axiosInstance);
            if (newAccessToken) {
                originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                return axiosInstance(originalRequest);
            }
        }

        return Promise.reject(error);
    }
);

export default axiosInstance;