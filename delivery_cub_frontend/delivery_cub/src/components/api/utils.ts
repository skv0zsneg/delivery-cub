export const saveTokens = (accessToken: string, refreshToken: string) => {
    sessionStorage.setItem('accessToken', accessToken);
    sessionStorage.setItem('refreshToken', refreshToken);
};

export const getAccessToken = (): string | null => {
    return sessionStorage.getItem('accessToken');
};

export const getRefreshToken = (): string | null => {
    return sessionStorage.getItem('refreshToken');
};

export const clearTokens = () => {
    sessionStorage.removeItem('accessToken');
    sessionStorage.removeItem('refreshToken');
};