import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Replace with your Django API base URL
});




// const refreshAccessToken = async (refreshToken) => {
//   try {
//     const response = await api.post('/api_auth/refresh/', {
//       refresh_token: refreshToken,
//     });
//     return response;

//   } catch (error) {
    
//     throw error;
//   }
// };

// let isRefreshing = false;

// const logoutUser = () => {
//   localStorage.removeItem('access_token');
//   localStorage.removeItem('refresh_token');
//   localStorage.clear();
//   window.location.href = '/login'; // Redirect to the login page
// };

api.interceptors.request.use(
  async (config) => {
    const accessToken = localStorage.getItem('access_token');

    if (accessToken) {
      // Add the access token to the request headers if available
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    return response;
  }
  ,
  async (error) => {
    const originalRequest = error.config;
    const refreshToken = localStorage.getItem('refresh_token');

    if (refreshToken && error.response.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        axios.
        post('http://localhost:8000/api_auth/refresh/', {
          refresh_token: refreshToken,
        })
        .then(response => {
          localStorage.setItem('access_token', response.data.access_token);
          localStorage.setItem('refresh_token', response.data.refresh_token);
          api.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
          originalRequest.headers['Authorization'] = `Bearer ${response.data.access_token}`;
          console.log('Access token refreshed!');
          return api(originalRequest);
        }
        )
        .catch(error => {
          console.log('Error refreshing access token', error);
          console.log(error);
        }
        );
      }
      isRefreshing = true;
      originalRequest._retry = true;
      const access_token = await refreshAccessToken(refreshToken);
      localStorage.setItem('access_token', access_token.data.access_token);
      localStorage.setItem('refresh_token', access_token.data.refresh_token);
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token.data.access_token}`;
      originalRequest.headers['Authorization'] = `Bearer ${access_token.data.access_token}`;
      isRefreshing = false;
      return api(originalRequest);
    }
    else if (error.response.status === 403) {
      logoutUser();
    }

    return Promise.reject(error);
  }
);

export default api;