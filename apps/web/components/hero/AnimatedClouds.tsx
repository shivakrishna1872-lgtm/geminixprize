import React from "react";
import { motion } from "framer-motion";

export function AnimatedClouds() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
      {/* Cloud 1 */}
      <motion.div
        animate={{ x: ["100vw", "-100vw"] }}
        transition={{ repeat: Infinity, duration: 60, ease: "linear" }}
        className="absolute top-[10%] opacity-20"
      >
        <svg width="200" height="100" viewBox="0 0 200 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M50 50 a30,30 0 0,1 60,0 a20,20 0 0,1 40,0 h-100 z" fill="white" className="pixelated" />
        </svg>
      </motion.div>
      
      {/* Cloud 2 */}
      <motion.div
        animate={{ x: ["100vw", "-100vw"] }}
        transition={{ repeat: Infinity, duration: 80, ease: "linear", delay: 20 }}
        className="absolute top-[25%] opacity-10 scale-150"
      >
        <svg width="200" height="100" viewBox="0 0 200 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M40 60 a20,20 0 0,1 40,0 a30,30 0 0,1 60,0 a15,15 0 0,1 30,0 h-130 z" fill="white" className="pixelated" />
        </svg>
      </motion.div>

      {/* Cloud 3 */}
      <motion.div
        animate={{ x: ["-50vw", "100vw"] }}
        transition={{ repeat: Infinity, duration: 100, ease: "linear", delay: 10 }}
        className="absolute top-[15%] opacity-15 scale-75"
      >
        <svg width="200" height="100" viewBox="0 0 200 100" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M50 50 a30,30 0 0,1 60,0 a20,20 0 0,1 40,0 h-100 z" fill="white" className="pixelated" />
        </svg>
      </motion.div>
    </div>
  );
}
