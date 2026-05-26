import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export const getAllLeads = () =>
  axios.get(`${BASE_URL}/leads/all`);

export const getHotLeads = () =>
  axios.get(`${BASE_URL}/leads/hot`);

export const getWarmLeads = () =>
  axios.get(`${BASE_URL}/leads/warm`);

export const getColdLeads = () =>
  axios.get(`${BASE_URL}/leads/cold`);

export const getStats = () =>
  axios.get(`${BASE_URL}/leads/stats`);

export const uploadLeadsCsv = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return axios.post(`${BASE_URL}/bulk-predict`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};