"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";

const EXAMPLE_PROMPTS = [
  "Build me a premium anime clothing brand.",
  "Launch a luxury candle subscription box.",
  "Create a minimalist productivity app store.",
  "Start a gourmet pet food brand.",
  "Build a sustainable streetwear brand.",
];

export function PromptInput() {
  const router = useRouter();
  const [prompt, setPrompt] = useState("");
  const [placeholderIndex, setPlaceholderIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPlaceholderIndex((prev) => (prev + 1) % EXAMPLE_PROMPTS.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleLaunch = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!prompt.trim()) return;
    router.push(`/launch?prompt=${encodeURIComponent(prompt)}`);
  };

  return (
    <div className="w-full max-w-3xl flex flex-col items-center">
      <form onSubmit={handleLaunch} className="w-full relative mb-12">
        <div className="relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-brand-purple to-brand-blue rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200" />
          <div className="relative flex items-center glass-card rounded-2xl p-2 bg-[#0a0a0f]/80">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder={EXAMPLE_PROMPTS[placeholderIndex]}
              className="w-full bg-transparent border-none text-white text-lg md:text-xl px-6 py-4 focus:outline-none focus:ring-0"
            />
            <button
              type="submit"
              disabled={!prompt.trim()}
              className="hidden md:flex items-center gap-2 px-8 py-4 bg-white text-black rounded-xl font-semibold hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Launch
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </button>
          </div>
        </div>
        
        <button
          type="submit"
          disabled={!prompt.trim()}
          className="md:hidden mt-4 w-full flex justify-center items-center gap-2 px-8 py-4 bg-white text-black rounded-xl font-semibold hover:bg-gray-200 transition-colors disabled:opacity-50"
        >
          Launch
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </button>
      </form>

      <div className="flex flex-wrap justify-center gap-3 w-full">
        {EXAMPLE_PROMPTS.slice(0, 3).map((ex, i) => (
          <button
            key={i}
            onClick={() => setPrompt(ex)}
            className="text-sm px-4 py-2 rounded-full glass-card text-gray-300 hover:text-white hover:bg-white/10 transition-colors"
          >
            &quot;{ex}&quot;
          </button>
        ))}
      </div>
    </div>
  );
}
