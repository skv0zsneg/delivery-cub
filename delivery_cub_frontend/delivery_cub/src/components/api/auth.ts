import { AxiosInstance } from 'axios';
import { TokenApi } from './openapi_generated/api';
import { saveTokens, getRefreshToken, clearTokens } from './utils';


export const login = async (username: string, password: string, axiosInstance: AxiosInstance) => {
    const tokenApi = new TokenApi(undefined, undefined, axiosInstance);
    try {
        const response = await tokenApi.tokenCreate({ username, password });
        const { access, refresh } = response.data;

        // Сохраняем токены
        saveTokens(access, refresh);

        return { success: true };
    } catch (error) {
        console.error('Login failed:', error);
        return { success: false, error: 'Invalid credentials' };
    }
};

export const refreshAccessToken = async (axiosInstance: AxiosInstance) => {
    const tokenApi = new TokenApi(undefined, undefined, axiosInstance);
    try {
        const refreshToken = getRefreshToken();
        if (!refreshToken) {
            throw new Error('No refresh token available');
        }

        const response = await tokenApi.tokenRefreshCreate({ refresh: refreshToken });
        const newAccessToken = response.data.access;

        // Обновляем только access-токен
        sessionStorage.setItem('accessToken', newAccessToken);

        return newAccessToken;
    } catch (error) {
        console.error('Token refresh failed:', error);
        clearTokens();
        return null;
    }
};