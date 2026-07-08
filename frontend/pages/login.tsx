import { FC, useState } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import { api } from '@/services/api';
import { useAppStore } from '@/store/app';
import toast from 'react-hot-toast';

const LoginPage: FC = () => {
  const router = useRouter();
  const { setAuth } = useAppStore();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (mode === 'register') {
        await api.register(username, password);
        toast.success('Account created — you can sign in now');
        setMode('login');
      } else {
        const token = await api.login(username, password);
        setAuth(
          {
            id: username,
            username,
            email: `${username}@offmap.app`,
            bio: 'Curious traveler',
            avatar: '',
            created_at: new Date().toISOString(),
          },
          token.access_token
        );
        toast.success('Signed in successfully');
        router.push('/');
      }
    } catch (error) {
      toast.error('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>OffMap | Sign In</title>
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-primary/10 via-white to-secondary/10 flex items-center justify-center px-4 py-20">
        <div className="w-full max-w-md rounded-3xl bg-white p-8 shadow-2xl">
          <div className="mb-8 text-center">
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-primary">OffMap</p>
            <h1 className="mt-2 text-3xl font-bold text-gray-900">{mode === 'login' ? 'Welcome back' : 'Create your account'}</h1>
            <p className="mt-2 text-sm text-gray-600">Start saving your next hidden gem.</p>
          </div>

          <div className="mb-6 flex rounded-full bg-gray-100 p-1">
            <button
              type="button"
              onClick={() => setMode('login')}
              className={`flex-1 rounded-full px-4 py-2 text-sm font-semibold transition ${mode === 'login' ? 'bg-white text-gray-900 shadow' : 'text-gray-600'}`}
            >
              Login
            </button>
            <button
              type="button"
              onClick={() => setMode('register')}
              className={`flex-1 rounded-full px-4 py-2 text-sm font-semibold transition ${mode === 'register' ? 'bg-white text-gray-900 shadow' : 'text-gray-600'}`}
            >
              Register
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              className="w-full rounded-xl border border-gray-200 px-4 py-3 outline-none focus:border-primary"
              required
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              className="w-full rounded-xl border border-gray-200 px-4 py-3 outline-none focus:border-primary"
              required
            />
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl bg-gradient-to-r from-primary to-secondary px-4 py-3 font-semibold text-white transition hover:shadow-lg disabled:opacity-70"
            >
              {loading ? 'Please wait...' : mode === 'login' ? 'Sign In' : 'Create Account'}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-600">
            <Link href="/" className="font-semibold text-primary">Back to home</Link>
          </p>
        </div>
      </main>
    </>
  );
};

export default LoginPage;
