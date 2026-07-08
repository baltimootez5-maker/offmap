/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#667eea',
        secondary: '#764ba2',
        accent: '#FFE66D',
        dark: '#1a1a2e',
        light: '#f8f9fa',
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', 'Oxygen', 'Ubuntu', 'sans-serif'],
      },
      boxShadow: {
        sm: '0 2px 8px rgba(0,0,0,0.08)',
        md: '0 8px 24px rgba(0,0,0,0.12)',
        lg: '0 16px 48px rgba(0,0,0,0.16)',
        xl: '0 20px 60px rgba(0,0,0,0.20)',
      },
      borderRadius: {
        'brand': '16px',
      },
      backdropBlur: {
        md: '10px',
        lg: '20px',
      },
      animation: {
        fadeIn: 'fadeIn 0.8s ease-out',
        slideDown: 'slideDown 0.8s ease-out',
        fadeInUp: 'fadeInUp 1s ease-out',
        drift: 'drift 20s linear infinite',
        pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideDown: {
          '0%': { opacity: '0', transform: 'translateY(-20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        drift: {
          '0%': { transform: 'translate(0, 0)' },
          '100%': { transform: 'translate(40px, 40px)' },
        },
      },
    },
  },
  plugins: [
    require('tailwindcss/plugin')(function ({ addComponents }) {
      addComponents({
        '.glass': {
          '@apply bg-white/30 backdrop-blur-md border border-white/20': {},
        },
        '.glass-dark': {
          '@apply bg-gray-900/30 backdrop-blur-md border border-gray-700/20': {},
        },
        '.btn-primary': {
          '@apply px-6 py-2 rounded-lg bg-gradient-to-r from-primary to-secondary text-white font-semibold hover:shadow-lg transform hover:-translate-y-1 transition-all': {},
        },
        '.btn-secondary': {
          '@apply px-6 py-2 rounded-lg bg-white text-gray-900 font-semibold border border-gray-200 hover:border-primary hover:text-primary transition-all': {},
        },
      });
    }),
  ],
};
