'use client';

import { useBusinessStore } from '@/stores/businessStore';
import { motion } from 'framer-motion';

export function WebsitePreview() {
  const { business } = useBusinessStore();
  const brand = business?.brand;
  const blueprint = business?.blueprint;
  const products = business?.products || [];

  if (!brand || !blueprint) {
    return (
      <div className="glass-card rounded-2xl p-6 h-96 flex flex-col items-center justify-center border-dashed border-2 border-white/10">
        <div className="text-4xl mb-4 animate-bounce">🌐</div>
        <h2 className="text-xl font-pixel text-gray-400">Awaiting Forge...</h2>
        <p className="text-sm text-gray-500 mt-2 text-center max-w-sm">
          The website preview will appear once the brand identity and blueprint are generated.
        </p>
      </div>
    );
  }

  // Dynamic CSS variables based on AI generated brand colors
  const style = {
    '--theme-primary': brand.primaryColor || '#000000',
    '--theme-secondary': brand.secondaryColor || '#ffffff',
    '--theme-accent': brand.accentColor || '#7C3AED',
  } as React.CSSProperties;

  return (
    <div className="glass-card rounded-2xl p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-display font-bold flex items-center gap-2">
          <span>💻</span> Live Store Preview
        </h2>
        {business.websiteUrl && (
          <a href={business.websiteUrl} target="_blank" rel="noreferrer" className="text-sm text-brand-cyan hover:underline font-pixel">
            Visit Store ↗
          </a>
        )}
      </div>

      <div className="border border-white/20 rounded-xl overflow-hidden bg-white text-black" style={style}>
        {/* Browser Header Mock */}
        <div className="bg-gray-200 border-b border-gray-300 px-4 py-2 flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-400" />
            <div className="w-3 h-3 rounded-full bg-yellow-400" />
            <div className="w-3 h-3 rounded-full bg-green-400" />
          </div>
          <div className="mx-auto bg-white rounded-md px-4 py-1 text-xs text-gray-500 w-1/2 text-center font-mono truncate">
            {business.websiteUrl || `https://${brand.name.toLowerCase().replace(/\\s+/g, '')}.com`}
          </div>
        </div>

        {/* Store Content Mock */}
        <div className="h-[400px] overflow-y-auto">
          {/* Hero Section */}
          <div 
            className="w-full py-16 px-8 text-center text-white relative"
            style={{ backgroundColor: 'var(--theme-primary)' }}
          >
            <h1 className="text-4xl font-bold mb-4" style={{ fontFamily: brand.fontHeading }}>
              {brand.name}
            </h1>
            <p className="text-xl opacity-90 mb-8" style={{ fontFamily: brand.fontBody }}>
              {brand.tagline || blueprint.value_proposition}
            </p>
            <button 
              className="px-8 py-3 rounded-full font-bold shadow-lg transition-transform hover:scale-105"
              style={{ backgroundColor: 'var(--theme-accent)', color: '#fff' }}
            >
              Shop Now
            </button>
          </div>

          {/* Products Section */}
          <div className="p-8 bg-gray-50">
            <h3 className="text-2xl font-bold mb-6 text-center" style={{ color: 'var(--theme-primary)' }}>Featured Collection</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
              {products.length > 0 ? (
                products.map((p, i) => (
                  <div key={i} className="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                    <div className="aspect-square bg-gray-200 rounded-md mb-4 flex items-center justify-center text-4xl">
                      🛍️
                    </div>
                    <h4 className="font-bold text-sm truncate">{p.name}</h4>
                    <p className="text-gray-500 text-xs mt-1" style={{ color: 'var(--theme-accent)' }}>
                      ${p.priceUsd?.toFixed(2) || '29.99'}
                    </p>
                  </div>
                ))
              ) : (
                /* Placeholders while products generate */
                [1,2,3].map(i => (
                  <div key={i} className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 animate-pulse">
                    <div className="aspect-square bg-gray-200 rounded-md mb-4" />
                    <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
                    <div className="h-3 bg-gray-200 rounded w-1/4" />
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
