import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000",
});

// Add token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = token;
  }
  return config;
});

// Handle expired session (403/401)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      localStorage.removeItem("token");
      window.location.href = "/"; // Redirect to login
    }
    return Promise.reject(error);
  }
);

export default api;
