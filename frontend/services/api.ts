import axios, { AxiosInstance, AxiosError } from 'axios';
import { AuthToken, Destination } from '@/lib/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class OffMapAPI {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add token to requests if available
    this.api.interceptors.request.use((config) => {
      const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // Auth endpoints
  async register(username: string, password: string): Promise<{ success: boolean }> {
    try {
      const response = await this.api.post('/auth/register', { username, password });
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async login(username: string, password: string): Promise<AuthToken> {
    try {
      const response = await this.api.post('/auth/login', { username, password });
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  // Wishlist endpoints
  async getWishlist(): Promise<string[]> {
    try {
      const response = await this.api.get('/wishlist');
      return response.data;
    } catch (error) {
      if ((error as AxiosError).response?.status === 401) {
        return []; // Return empty if not authenticated
      }
      this.handleError(error);
      throw error;
    }
  }

  async addToWishlist(name: string): Promise<{ added: string }> {
    try {
      const response = await this.api.post('/wishlist', { name });
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async removeFromWishlist(name: string): Promise<{ deleted: string }> {
    try {
      const response = await this.api.delete(`/wishlist/${name}`);
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  // Destinations (future endpoint)
  async getDestinations(): Promise<Destination[]> {
    try {
      // For now, return mock data
      // Later this will fetch from backend
      return [];
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  private handleError(error: unknown): void {
    if (axios.isAxiosError(error)) {
      console.error('API Error:', error.response?.data || error.message);
    } else {
      console.error('Unexpected error:', error);
    }
  }
}

export const api = new OffMapAPI();
