import axios from "axios";

const apiClient = axios.create({
  // Later read this URL from an environment variable
  baseURL: "/api",
});

export default apiClient;
