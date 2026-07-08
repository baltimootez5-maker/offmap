// Type definitions for OffMap

export interface Destination {
  id: string;
  name: string;
  country: string;
  desc: string;
  img: string;
  remote_img: string;
  tags: string[];
  mood: string;
  price: string;
  rating?: number;
  reviews?: number;
}

export interface User {
  id: string;
  username: string;
  email: string;
  avatar?: string;
  bio?: string;
  created_at: string;
}

export interface Wishlist {
  id: string;
  user_id: string;
  destination_id: string;
  created_at: string;
}

export interface TravelJournal {
  id: string;
  user_id: string;
  destination_id: string;
  title: string;
  description: string;
  photos: string[];
  rating: number;
  visited_date: string;
  created_at: string;
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  unlocked: boolean;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}
