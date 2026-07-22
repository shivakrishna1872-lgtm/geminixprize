import React from "react";
import { motion } from "framer-motion";

export function PixelSkyline() {
  return (
    <div className="absolute bottom-0 left-0 right-0 h-64 overflow-hidden pointer-events-none z-0 opacity-40">
      <div className="relative w-full h-full flex items-end justify-around px-10">
        
        {/* Building 1 */}
        <motion.div 
          initial={{ y: 200 }} 
          animate={{ y: 0 }} 
          transition={{ duration: 1.2, ease: "easeOut" }}
          className="w-24 h-48 bg-[#1A1A2E] border-t-2 border-l-2 border-r-2 border-brand-purple flex flex-wrap content-start p-2 gap-2"
        >
          {Array.from({ length: 12 }).map((_, i) => (
            <div key={i} className={`w-4 h-4 ${i % 3 === 0 ? 'bg-brand-cyan glow-blue' : 'bg-black/50'} rounded-sm`} />
          ))}
        </motion.div>

        {/* Building 2 (Tall) */}
        <motion.div 
          initial={{ y: 300 }} 
          animate={{ y: 0 }} 
          transition={{ duration: 1.5, ease: "easeOut", delay: 0.2 }}
          className="w-32 h-64 bg-[#16213E] border-t-2 border-l-2 border-r-2 border-brand-blue flex flex-col items-center pt-2 relative"
        >
          {/* Antenna */}
          <div className="absolute -top-10 w-1 h-10 bg-brand-cyan" />
          <div className="absolute -top-12 w-3 h-3 bg-red-500 rounded-full animate-pulse" />
          
          <div className="w-full h-full flex flex-wrap content-start justify-center gap-3 mt-4">
            {Array.from({ length: 18 }).map((_, i) => (
              <div key={i} className={`w-6 h-4 ${i % 2 === 0 ? 'bg-brand-purple opacity-80' : 'bg-black/50'} rounded-sm`} />
            ))}
          </div>
          
          {/* Rooftop Character */}
          <div className="absolute -top-8 left-4 flex flex-col items-center">
            {/* Body */}
            <div className="w-4 h-6 bg-brand-pink" />
            {/* Head */}
            <div className="w-4 h-4 bg-white rounded-sm -mt-10" />
            {/* Laptop Glow */}
            <div className="absolute top-2 left-6 w-3 h-2 bg-brand-cyan glow-blue rounded-sm" />
          </div>
        </motion.div>

        {/* Building 3 */}
        <motion.div 
          initial={{ y: 150 }} 
          animate={{ y: 0 }} 
          transition={{ duration: 1.0, ease: "easeOut", delay: 0.1 }}
          className="w-40 h-32 bg-[#0F3460] border-t-2 border-l-2 border-r-2 border-brand-pink flex flex-wrap content-start p-3 gap-3"
        >
           {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className={`w-8 h-4 ${i % 3 !== 0 ? 'bg-white opacity-90 glow-purple' : 'bg-black/50'} rounded-sm`} />
          ))}
        </motion.div>

      </div>
      
      {/* Ground Line */}
      <div className="absolute bottom-0 w-full h-2 bg-gradient-to-r from-brand-purple via-brand-cyan to-brand-blue opacity-50" />
    </div>
  );
}
