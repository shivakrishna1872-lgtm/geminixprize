import React from "react";
import { motion, HTMLMotionProps } from "framer-motion";

interface GlassCardProps extends HTMLMotionProps<"div"> {
  children: React.ReactNode;
  className?: string;
  hoverEffect?: boolean;
}

export function GlassCard({ children, className = "", hoverEffect = false, ...props }: GlassCardProps) {
  return (
    <motion.div
      whileHover={hoverEffect ? { y: -5, transition: { duration: 0.2 } } : undefined}
      className={`glass-card rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl ${className}`}
      {...props}
    >
      {children}
    </motion.div>
  );
}
