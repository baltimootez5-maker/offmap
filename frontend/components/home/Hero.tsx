import { FC } from 'react';
import { motion } from 'framer-motion';

interface HeroProps {
  onSearchChange?: (value: string) => void;
}

const Hero: FC<HeroProps> = ({ onSearchChange }) => {
  return (
    <section className="relative w-full min-h-screen bg-gradient-to-br from-primary via-secondary to-purple-900 overflow-hidden flex items-center justify-center">
      {/* Background grid animation */}
      <div className="absolute inset-0 opacity-10">
        <svg
          className="w-full h-full animate-drift"
          viewBox="0 0 1200 600"
        >
          <defs>
            <pattern
              id="grid"
              width="40"
              height="40"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M 40 0 L 0 0 0 40"
                fill="none"
                stroke="white"
                strokeWidth="1"
              />
            </pattern>
          </defs>
          <rect width="1200" height="600" fill="url(#grid)" />
        </svg>
      </div>

      {/* Content */}
      <div className="relative z-10 text-center text-white px-4 py-20 max-w-4xl mx-auto">
        {/* Title */}
        <motion.h1
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          className="text-6xl md:text-7xl font-bold mb-6 tracking-tight leading-tight"
        >
          ✨ OffMap
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 0.3 }}
          className="text-xl md:text-2xl font-light mb-12 text-white/90 max-w-2xl mx-auto"
        >
          Discover hidden gems off the beaten path — curated for curious travelers
        </motion.p>

        {/* Search Box */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.5 }}
          className="flex gap-2 glass backdrop-blur-md p-3 rounded-2xl max-w-md mx-auto shadow-2xl"
        >
          <input
            type="text"
            placeholder="🌍 Where's your next adventure?"
            onChange={(e) => onSearchChange?.(e.target.value)}
            className="flex-1 bg-transparent text-gray-900 placeholder-gray-500 outline-none font-medium"
          />
          <button className="btn-primary px-6 py-2 rounded-lg font-semibold">
            Explore
          </button>
        </motion.div>

        {/* CTA */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 0.8 }}
          className="mt-12 text-white/70 text-sm font-medium"
        >
          Explore thousands of hidden destinations around the world ↓
        </motion.p>
      </div>
    </section>
  );
};

export default Hero;
