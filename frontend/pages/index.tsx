import { FC, useState } from 'react';
import type { GetStaticProps } from 'next';
import Head from 'next/head';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import Hero from '@/components/home/Hero';
import DestinationCard from '@/components/cards/DestinationCard';
import { Destination } from '@/lib/types';
import { useAppStore } from '@/store/app';

// Mock data - replace with API calls
const DESTINATIONS: Destination[] = [
  {
    id: '1',
    name: 'Kawah Ijen Blue Fire',
    country: 'Indonesia',
    desc: 'A volcanic crater famous for electric-blue flames and sulfur miners.',
    img: 'assets/kawah_ijen.png',
    remote_img: 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80',
    tags: ['volcano', 'adventure'],
    mood: 'Adventure',
    price: '€450-650',
    rating: 4.8,
    reviews: 234,
  },
  {
    id: '2',
    name: 'Svaneti Villages',
    country: 'Georgia',
    desc: 'Remote mountain villages with medieval towers and alpine trails.',
    img: 'assets/svaneti.png',
    remote_img: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1200&q=80',
    tags: ['mountains', 'culture'],
    mood: 'Cultural',
    price: '€300-500',
    rating: 4.7,
    reviews: 189,
  },
  {
    id: '3',
    name: 'Islas Cies',
    country: 'Spain',
    desc: 'Pristine beaches and crystal waters on a protected island archipelago.',
    img: 'assets/islas_cies.png',
    remote_img: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80',
    tags: ['beach', 'relax'],
    mood: 'Relaxing',
    price: '€250-400',
    rating: 4.9,
    reviews: 312,
  },
  {
    id: '4',
    name: 'Valle de Viñales',
    country: 'Cuba',
    desc: 'Limestone mogotes, tobacco farms, and colorful rural life.',
    img: 'assets/vinales.png',
    remote_img: 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=1200&q=80',
    tags: ['nature', 'culture'],
    mood: 'Adventure',
    price: '€350-550',
    rating: 4.6,
    reviews: 156,
  },
  {
    id: '5',
    name: 'Cappadocia Hot Air Balloons',
    country: 'Turkey',
    desc: 'Ancient cave dwellings, fairy chimneys, and sunrise hot air balloon rides over surreal landscapes.',
    img: 'assets/cappadocia.png',
    remote_img: 'https://images.unsplash.com/photo-1493246507139-91e8fad9978e?auto=format&fit=crop&w=1200&q=80',
    tags: ['adventure', 'scenic'],
    mood: 'Hidden Gem',
    price: '€400-700',
    rating: 4.9,
    reviews: 425,
  },
];

interface HomeProps {
  destinations: Destination[];
}

const Home: FC<HomeProps> = ({ destinations }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCountry, setSelectedCountry] = useState('All');
  const { wishlist, addToWishlist } = useAppStore();

  const countries = ['All', ...new Set(destinations.map((d) => d.country))];

  const filteredDestinations = destinations.filter((dest) => {
    const matchesSearch = dest.name
      .toLowerCase()
      .includes(searchQuery.toLowerCase()) ||
      dest.desc.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCountry =
      selectedCountry === 'All' || dest.country === selectedCountry;
    return matchesSearch && matchesCountry;
  });

  return (
    <>
      <Head>
        <title>OffMap - Discover Hidden Gems</title>
        <meta
          name="description"
          content="AI-powered travel discovery platform for hidden gems and authentic experiences"
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <Header />

      <main>
        {/* Hero Section */}
        <Hero onSearchChange={setSearchQuery} />

        {/* Destinations Section */}
        <section className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <div className="mb-12">
            <h2 className="text-4xl md:text-5xl font-bold mb-4 text-center">
              🗺️ Hidden Gems Await
            </h2>
            <p className="text-center text-gray-600 text-lg max-w-2xl mx-auto">
              Carefully curated destinations for the curious traveler. Filter by country or search for your next adventure.
            </p>
          </div>

          {/* Filters */}
          <div className="mb-8 flex flex-wrap gap-3 justify-center">
            {countries.map((country) => (
              <button
                key={country}
                onClick={() => setSelectedCountry(country)}
                className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                  selectedCountry === country
                    ? 'bg-gradient-to-r from-primary to-secondary text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {country}
              </button>
            ))}
          </div>

          {/* Grid */}
          {filteredDestinations.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {filteredDestinations.map((dest) => (
                <DestinationCard
                  key={dest.id}
                  destination={dest}
                  onSave={addToWishlist}
                  isSaved={wishlist.some((w) => w.id === dest.id)}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">
                No destinations match your search. Try adjusting your filters!
              </p>
            </div>
          )}
        </section>

        {/* CTA Section */}
        <section className="bg-gradient-to-r from-primary to-secondary text-white py-16 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl font-bold mb-4">Ready to Explore?</h2>
            <p className="text-xl mb-8 text-white/90">
              Join thousands of travelers discovering authentic experiences beyond the guidebook.
            </p>
            <button className="bg-white text-primary hover:text-secondary font-bold py-3 px-8 rounded-lg hover:shadow-lg transform hover:-translate-y-1 transition-all">
              Start Exploring Now
            </button>
          </div>
        </section>
      </main>

      <Footer />
    </>
  );
};

export const getStaticProps: GetStaticProps = async () => {
  return {
    props: {
      destinations: DESTINATIONS,
    },
    revalidate: 3600,
  };
};

export default Home;
