import axios from 'axios';
import type { ResourceInfo, AllResourcesStatus, ActionResponse } from '../types/resource';

const VITE_API_URL = import.meta.env.VITE_API_URL;
const VITE_API_URL_DEFAULT = 'http://localhost:8000';
const API_BASE_URL = VITE_API_URL || VITE_API_URL_DEFAULT;

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Get current system username
  async getUsername(): Promise<string> {
    const response = await api.get<{ username: string }>('/api/whoami');
    return response.data.username;
  },

  // Get all resources status
  async getAllStatus(): Promise<AllResourcesStatus> {
    const response = await api.get<AllResourcesStatus>('/status');
    return response.data;
  },

  // Publishers
  async getAllPublishers(): Promise<Record<string, ResourceInfo>> {
    const response = await api.get<Record<string, ResourceInfo>>('/publishers');
    return response.data;
  },

  async takePublisher(publisherId: string, user: string): Promise<ActionResponse> {
    const response = await api.post<ActionResponse>(`/publishers/take/${publisherId}?user=${user}`);
    return response.data;
  },

  async releasePublisher(publisherId: string): Promise<ActionResponse> {
    const response = await api.post<ActionResponse>(`/publishers/release/${publisherId}`);
    return response.data;
  },

  async stealPublisher(publisherId: string, user: string): Promise<ActionResponse> {
    const response = await api.post<ActionResponse>(`/publishers/steal/${publisherId}?user=${user}`);
    return response.data;
  },

  // Environments
  async getAllEnvironments(): Promise<Record<string, ResourceInfo>> {
    const response = await api.get<Record<string, ResourceInfo>>('/environments');
    return response.data;
  },

  async takeEnvironment(envName: string, user: string): Promise<ActionResponse> {
    const response = await api.post<ActionResponse>(`/environments/take/${envName}?user=${user}`);
    return response.data;
  },

  async releaseEnvironment(envName: string): Promise<ActionResponse> {
    const response = await api.post<ActionResponse>(`/environments/release/${envName}`);
    return response.data;
  },

  async stealEnvironment(envName: string, user: string): Promise<ActionResponse> {
    const response = await api.post<ActionResponse>(`/environments/steal/${envName}?user=${user}`);
    return response.data;
  },
};
