import type { Config } from "tailwindcss";

export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        brand: {
          purple: "#7C3AED",
          blue: "#2563EB",
          cyan: "#06B6D4",
          pink: "#EC4899",
        },
        bg: {
          dark: "#0A0A0F",
          glass: "rgba(255, 255, 255, 0.05)",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)"],
        display: ["var(--font-outfit)"],
      },
      animation: {
        float: "float 3s ease-in-out infinite",
        "pulse-glow": "pulse-glow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        marquee: "marquee 20s linear infinite",
        rain: "rain 1s linear infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
        "pulse-glow": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
        marquee: {
          "0%": { transform: "translateX(0%)" },
          "100%": { transform: "translateX(-100%)" },
        },
        rain: {
          "0%": { transform: "translateY(-10px)", opacity: "0" },
          "50%": { opacity: "1" },
          "100%": { transform: "translateY(100vh)", opacity: "0" },
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
