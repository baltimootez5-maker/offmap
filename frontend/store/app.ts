import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Destination, User } from '@/lib/types';
import { api } from '@/services/api';

interface AppStore {
  // Auth
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User | null, token: string | null) => void;
  logout: () => void;

  // Wishlist
  wishlist: Destination[];
  addToWishlist: (destination: Destination) => Promise<void>;
  removeFromWishlist: (id: string) => Promise<void>;

  // UI
  isDarkMode: boolean;
  toggleDarkMode: () => void;

  // Search
  searchQuery: string;
  setSearchQuery: (query: string) => void;

  // Filters
  selectedCountry: string;
  selectedTags: string[];
  setSelectedCountry: (country: string) => void;
  setSelectedTags: (tags: string[]) => void;
}

export const useAppStore = create<AppStore>()(
  persist(
    (set, get) => ({
      // Auth
      user: null,
      token: null,
      isAuthenticated: false,
      setAuth: (user, token) => {
        if (typeof window !== 'undefined') {
          if (token) {
            localStorage.setItem('access_token', token);
          } else {
            localStorage.removeItem('access_token');
          }
        }
        set({ user, token, isAuthenticated: !!token });
      },
      logout: () => {
        if (typeof window !== 'undefined') {
          localStorage.removeItem('access_token');
        }
        set({ user: null, token: null, isAuthenticated: false, wishlist: [] });
      },

      // Wishlist
      wishlist: [],
      addToWishlist: async (destination) => {
        const state = get();
        if (state.wishlist.some((item) => item.id === destination.id)) {
          return;
        }

        if (state.isAuthenticated && state.token) {
          try {
            await api.addToWishlist(destination.name);
          } catch (error) {
            console.error('Could not save to backend wishlist', error);
          }
        }

        set((current) => ({
          wishlist: [...current.wishlist, destination],
        }));
      },
      removeFromWishlist: async (id) => {
        const state = get();
        const destination = state.wishlist.find((item) => item.id === id);

        if (destination && state.isAuthenticated && state.token) {
          try {
            await api.removeFromWishlist(destination.name);
          } catch (error) {
            console.error('Could not remove from backend wishlist', error);
          }
        }

        set((current) => ({
          wishlist: current.wishlist.filter((item) => item.id !== id),
        }));
      },

      // UI
      isDarkMode: false,
      toggleDarkMode: () =>
        set((state) => ({ isDarkMode: !state.isDarkMode })),

      // Search
      searchQuery: '',
      setSearchQuery: (query) => set({ searchQuery: query }),

      // Filters
      selectedCountry: 'All',
      selectedTags: [],
      setSelectedCountry: (country) =>
        set({ selectedCountry: country }),
      setSelectedTags: (tags) =>
        set({ selectedTags: tags }),
    }),
    {
      name: 'offmap-store',
    }
  )
);
