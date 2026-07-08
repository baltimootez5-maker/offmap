# OffMap Frontend - React/Next.js

Production-ready travel discovery platform frontend built with React 18, Next.js 14, TypeScript, and Tailwind CSS.

## 🚀 Features

- ✨ Beautiful, responsive UI (mobile-first design)
- 🎨 Modern animations with Framer Motion
- 🔐 Authentication ready (JWT integration)
- 🌐 Global state management (Zustand)
- 📱 Mobile-optimized (iOS, Android)
- 🎯 Performance optimized (Next.js static generation)
- 🌙 Dark mode support (built-in)
- ♿ Accessibility first
- 📊 Analytics-ready
- 🔌 API integration layer (FastAPI backend)

## 📋 Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS + custom components
- **Animations**: Framer Motion
- **State**: Zustand
- **HTTP**: Axios
- **UI Icons**: React Icons
- **Toast Notifications**: React Hot Toast
- **Linting**: ESLint + Prettier

## 🏗️ Project Structure

```
frontend/
├── pages/               # Next.js pages (routing)
├── components/          # Reusable React components
│   ├── home/           # Homepage components
│   ├── cards/          # Card components
│   └── layout/         # Layout components
├── services/           # API communication
├── store/              # Global state (Zustand)
├── lib/                # Utilities and types
├── hooks/              # Custom React hooks
├── utils/              # Helper functions
├── styles/             # Global CSS
└── public/             # Static assets

```

## 🔧 Installation

```bash
cd frontend
npm install
# or
yarn install
```

## 🚀 Development

```bash
npm run dev
```

Visit `http://localhost:3000` in your browser.

## 📦 Build for Production

```bash
npm run build
npm start
```

## 📝 Configuration

### Environment Variables

Create `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=OffMap
```

### Tailwind CSS

Customized in `tailwind.config.js` with:
- Custom color palette
- Glassmorphism effects
- Animation keyframes
- Component utilities

## 🎨 Component Library

### Pages
- `pages/index.tsx` - Homepage
- `pages/explore.tsx` - Destination explore page
- `pages/login.tsx` - Authentication
- `pages/wishlist.tsx` - User wishlist

### Components
- `Hero.tsx` - Main landing hero section
- `DestinationCard.tsx` - Destination card with actions
- `Header.tsx` - Navigation header
- `Footer.tsx` - Site footer

## 🔗 API Integration

All API calls through `services/api.ts`:

```typescript
import { api } from '@/services/api';

// Login
const token = await api.login(username, password);

// Get wishlist
const wishlist = await api.getWishlist();

// Add to wishlist
await api.addToWishlist(destinationName);
```

## 🌐 Deployment

### Vercel (Recommended)

```bash
vercel
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
CMD npm start
```

### Environment Variables for Production

- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NEXT_PUBLIC_APP_NAME` - App name

## 📚 Code Style

- ESLint configured
- Prettier formatter (`npm run format`)
- TypeScript strict mode
- Naming conventions enforced

## 🧪 Performance

- Static generation (ISR)
- Image optimization
- Code splitting
- Bundle size optimized
- Lighthouse score target: 90+

## 📱 Responsive Design

- Mobile-first approach
- Tailwind breakpoints
- Touch-friendly buttons
- Optimized images

## 🔐 Security

- CORS configured
- JWT token handling
- Secure storage (localStorage with cleanup)
- Input sanitization
- Headers optimization

## 🚦 Next Steps

1. ✅ Frontend setup complete
2. ⏳ Connect to FastAPI backend
3. ⏳ Add authentication pages
4. ⏳ Implement interactive map
5. ⏳ Add AI integration
6. ⏳ Build premium features
7. ⏳ Deploy to production

## 📖 Documentation

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion/)
- [Zustand](https://github.com/pmndrs/zustand)

## 📞 Support

For issues or questions, contact the development team.

---

**Status**: Production-Ready Foundation ✅  
**Version**: 1.0.0  
**Last Updated**: 2024
