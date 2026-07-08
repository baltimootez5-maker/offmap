import { FC } from 'react';
import Link from 'next/link';
import { useAppStore } from '@/store/app';
import { FiLogOut, FiHeart } from 'react-icons/fi';

const Header: FC = () => {
  const { isAuthenticated, user, logout } = useAppStore();

  return (
    <header className="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-gray-200/50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <div className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent group-hover:scale-110 transition-transform">
              ✨ OffMap
            </div>
          </Link>

          {/* Nav Links */}
          <nav className="hidden md:flex items-center gap-8">
            <Link href="/explore" className="text-gray-700 hover:text-primary font-medium transition">
              Explore
            </Link>
            <Link href="/map" className="text-gray-700 hover:text-primary font-medium transition">
              Map
            </Link>
            {isAuthenticated && (
              <Link href="/journal" className="text-gray-700 hover:text-primary font-medium transition">
                Journal
              </Link>
            )}
          </nav>

          {/* Right Actions */}
          <div className="flex items-center gap-4">
            {isAuthenticated ? (
              <>
                <Link
                  href="/wishlist"
                  className="p-2 hover:bg-gray-100 rounded-lg transition"
                >
                  <FiHeart size={20} className="text-primary" />
                </Link>
                <div className="flex items-center gap-2 pl-4 border-l border-gray-200">
                  <span className="text-sm font-medium text-gray-700">
                    {user?.username}
                  </span>
                  <button
                    onClick={logout}
                    className="p-2 hover:bg-gray-100 rounded-lg transition"
                  >
                    <FiLogOut size={20} />
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link href="/login" className="btn-secondary px-4 py-2 rounded-lg">
                  Sign In
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
