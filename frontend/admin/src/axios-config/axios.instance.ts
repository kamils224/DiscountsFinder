import axios from "axios";
import config from "../config.local.json"

const axiosInstance = axios.create({baseURL: config.baseUrl})

export default axiosInstance;
