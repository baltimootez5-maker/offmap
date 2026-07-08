import { FC, useState } from 'react';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { Destination } from '@/lib/types';
import { FiHeart, FiMapPin, FiInfo } from 'react-icons/fi';
import toast from 'react-hot-toast';

interface DestinationCardProps {
  destination: Destination;
  onSave?: (destination: Destination) => Promise<void> | void;
  onDetails?: (destination: Destination) => void;
  isSaved?: boolean;
}

const DestinationCard: FC<DestinationCardProps> = ({
  destination,
  onSave,
  onDetails,
  isSaved,
}) => {
  const [isHovering, setIsHovering] = useState(false);

  const handleSave = async () => {
    await onSave?.(destination);
    toast.success(`Saved ${destination.name}!`);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      whileHover={{ y: -12, scale: 1.02 }}
      onMouseEnter={() => setIsHovering(true)}
      onMouseLeave={() => setIsHovering(false)}
      className="bg-white rounded-2xl shadow-sm hover:shadow-2xl transition-all duration-300 overflow-hidden cursor-pointer group"
    >
      {/* Image Container */}
      <div className="relative w-full h-56 overflow-hidden bg-gray-200">
        <Image
          src={destination.remote_img}
          alt={destination.name}
          fill
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
          onError={(e) => {
            (e.currentTarget as HTMLImageElement).src = destination.img;
          }}
        />
        {/* Overlay on hover */}
        {isHovering && (
          <div className="absolute inset-0 bg-black/30 backdrop-blur-sm" />
        )}
        {/* Mood tag */}
        <div className="absolute top-4 right-4">
          <span className="inline-block bg-gradient-to-r from-primary to-secondary text-white px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide">
            {destination.mood}
          </span>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {/* Location */}
        <div className="flex items-center gap-2 text-gray-500 text-sm mb-3">
          <FiMapPin size={16} />
          <span>{destination.country}</span>
          <span className="mx-1">•</span>
          <span className="font-semibold text-primary">{destination.price}</span>
        </div>

        {/* Title */}
        <h3 className="text-xl font-bold text-gray-900 mb-2 line-clamp-2">
          {destination.name}
        </h3>

        {/* Description */}
        <p className="text-gray-600 text-sm mb-4 line-clamp-2 leading-relaxed">
          {destination.desc}
        </p>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-4">
          {destination.tags.map((tag) => (
            <span
              key={tag}
              className="inline-block bg-gray-100 text-gray-700 px-2 py-1 rounded-lg text-xs font-semibold hover:bg-primary hover:text-white transition-colors"
            >
              {tag}
            </span>
          ))}
        </div>

        {/* Actions */}
        <div className="flex gap-2">
          <button
            onClick={() => void handleSave()}
            className={`flex-1 flex items-center justify-center gap-2 py-2 rounded-lg font-semibold transition-all ${
              isSaved
                ? 'bg-red-100 text-red-600 hover:bg-red-200'
                : 'bg-gradient-to-r from-primary to-secondary text-white hover:shadow-lg hover:-translate-y-1'
            }`}
          >
            <FiHeart size={18} fill={isSaved ? 'currentColor' : 'none'} />
            {isSaved ? 'Saved' : 'Save'}
          </button>
          <button
            onClick={() => onDetails?.(destination)}
            className="flex-1 flex items-center justify-center gap-2 py-2 rounded-lg font-semibold border-2 border-gray-200 text-gray-900 hover:border-primary hover:text-primary transition-all"
          >
            <FiInfo size={18} />
            Details
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default DestinationCard;
