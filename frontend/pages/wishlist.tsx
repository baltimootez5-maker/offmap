import { FC, useEffect, useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useAppStore } from '@/store/app';
import { FiArrowLeft, FiHeart } from 'react-icons/fi';
import { Destination } from '@/lib/types';

const WishlistPage: FC = () => {
  const { wishlist, isAuthenticated, removeFromWishlist } = useAppStore();
  const [items, setItems] = useState<Destination[]>([]);

  useEffect(() => {
    setItems(wishlist);
  }, [wishlist]);

  if (!isAuthenticated) {
    return (
      <>
        <Head><title>OffMap | Wishlist</title></Head>
        <main className="min-h-screen bg-gray-50 px-4 py-24">
          <div className="mx-auto max-w-2xl rounded-3xl bg-white p-10 text-center shadow-xl">
            <h1 className="text-3xl font-bold text-gray-900">Your wishlist awaits</h1>
            <p className="mt-3 text-gray-600">Sign in to save and revisit your favorite places.</p>
            <Link href="/login" className="mt-6 inline-flex rounded-full bg-gradient-to-r from-primary to-secondary px-6 py-3 font-semibold text-white">Sign in</Link>
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <Head><title>OffMap | Wishlist</title></Head>
      <main className="min-h-screen bg-gray-50 px-4 py-24">
        <div className="mx-auto max-w-6xl">
          <Link href="/" className="mb-8 inline-flex items-center gap-2 text-sm font-semibold text-primary">
            <FiArrowLeft /> Back to explore
          </Link>
          <div className="mb-8 flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">Wishlist</p>
              <h1 className="text-3xl font-bold text-gray-900">Saved destinations</h1>
            </div>
            <div className="rounded-full bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm">
              {items.length} saved
            </div>
          </div>

          {items.length === 0 ? (
            <div className="rounded-3xl bg-white p-10 text-center shadow-xl">
              <FiHeart className="mx-auto mb-4 text-4xl text-primary" />
              <h2 className="text-xl font-semibold text-gray-900">No saved destinations yet</h2>
              <p className="mt-2 text-gray-600">Start exploring and tap Save to build your dream list.</p>
            </div>
          ) : (
            <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
              {items.map((item) => (
                <div key={item.id} className="rounded-3xl bg-white p-6 shadow-lg">
                  <h3 className="text-xl font-semibold text-gray-900">{item.name}</h3>
                  <p className="mt-2 text-sm text-gray-600">{item.country}</p>
                  <p className="mt-4 text-sm text-gray-600">{item.desc}</p>
                  <button
                    onClick={() => void removeFromWishlist(item.id)}
                    className="mt-6 rounded-full bg-red-50 px-4 py-2 text-sm font-semibold text-red-600"
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </>
  );
};

export default WishlistPage;
