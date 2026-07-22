"use client";

import { motion } from "framer-motion";
import { GlassCard } from "@/components/shared/GlassCard";
import { AnimatedClouds } from "@/components/hero/AnimatedClouds";
import { PixelSkyline } from "@/components/hero/PixelSkyline";
import { PromptInput } from "@/components/hero/PromptInput";

const AGENTS = [
  { id: 'atlas', name: 'Atlas', role: 'CEO', emoji: '🧠', desc: 'Strategy & Coordination' },
  { id: 'nova', name: 'Nova', role: 'Designer', emoji: '🎨', desc: 'Brand Identity & UI' },
  { id: 'forge', name: 'Forge', role: 'Engineer', emoji: '⚙️', desc: 'Build & Deploy' },
  { id: 'pulse', name: 'Pulse', role: 'Marketing', emoji: '📢', desc: 'Copy & Campaigns' },
  { id: 'orbit', name: 'Orbit', role: 'Operations', emoji: '🔄', desc: 'Logistics & Supply' },
  { id: 'vault', name: 'Vault', role: 'Finance', emoji: '💰', desc: 'Payments & Pricing' },
  { id: 'echo', name: 'Echo', role: 'Support', emoji: '🎧', desc: 'Policies & FAQ' },
  { id: 'insight', name: 'Insight', role: 'Analytics', emoji: '📊', desc: 'Data & Growth' },
];

export default function LandingPage() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-bg-dark flex flex-col">
      {/* Dynamic Hero Background */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-brand-purple blur-[120px] opacity-20 animate-pulse-glow" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-brand-blue blur-[120px] opacity-20 animate-pulse-glow" style={{ animationDelay: "1s" }} />
        
        <AnimatedClouds />
        
        {/* CSS Rain */}
        {Array.from({ length: 20 }).map((_, i) => (
          <div
            key={i}
            className="absolute w-[1px] h-20 bg-gradient-to-b from-transparent to-brand-cyan opacity-30 animate-rain"
            style={{
              left: `${(i * 17) % 100}%`,
              animationDelay: `${(i * 3) % 5}s`,
              animationDuration: `${0.5 + (i % 2)}s`,
            }}
          />
        ))}

        <PixelSkyline />
      </div>

      <main className="relative z-10 flex-1 flex flex-col items-center pt-32 px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="flex flex-col items-center text-center max-w-4xl w-full"
        >
          <div className="mb-8 px-4 py-1.5 rounded-full glass-card text-sm font-medium text-brand-cyan tracking-wider uppercase inline-flex items-center gap-2 glow-blue">
            <span className="w-2 h-2 rounded-full bg-brand-cyan animate-pulse" />
            Google Gemini XPRIZE 2026
          </div>

          <h1 className="text-5xl md:text-7xl lg:text-8xl font-display font-bold tracking-tight mb-6">
            Build your <span className="gradient-text">next company.</span>
          </h1>

          <p className="text-xl md:text-2xl text-gray-400 mb-12 max-w-2xl font-sans">
            Describe your idea. Watch AI build, launch, and run it.
          </p>

          <PromptInput />
        </motion.div>
      </main>

      {/* Agents Section */}
      <section className="relative z-10 w-full max-w-6xl mx-auto px-6 py-32 mt-20">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8 }}
        >
          <h2 className="text-3xl md:text-5xl font-display font-bold text-center mb-16">
            Meet your <span className="gradient-text">AI team</span>
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {AGENTS.map((agent) => (
              <GlassCard key={agent.id} hoverEffect className="p-6 flex flex-col items-start gap-4">
                <div className="text-4xl">{agent.emoji}</div>
                <div>
                  <h3 className="text-xl font-bold font-display">{agent.name}</h3>
                  <div className="text-brand-cyan text-sm font-medium mb-2">{agent.role}</div>
                  <p className="text-gray-400 text-sm">{agent.desc}</p>
                </div>
              </GlassCard>
            ))}
          </div>
        </motion.div>
      </section>

      {/* How It Works Section */}
      <section className="relative z-10 w-full bg-black/40 border-t border-white/5 py-24">
        <div className="max-w-6xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
            transition={{ duration: 0.8 }}
            className="flex flex-col items-center"
          >
            <h2 className="text-3xl md:text-5xl font-display font-bold text-center mb-16">
              How it <span className="gradient-text">works</span>
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center w-full relative">
              <div className="hidden md:block absolute top-1/2 left-[15%] right-[15%] h-[1px] bg-gradient-to-r from-transparent via-brand-purple to-transparent -z-10" />
              
              <div className="flex flex-col items-center">
                <div className="w-16 h-16 rounded-full bg-bg-dark border-2 border-brand-purple flex items-center justify-center text-2xl mb-6 glow-purple">1</div>
                <h3 className="text-xl font-bold mb-2">Describe</h3>
                <p className="text-gray-400">Type your business idea in plain English.</p>
              </div>
              
              <div className="flex flex-col items-center">
                <div className="w-16 h-16 rounded-full bg-bg-dark border-2 border-brand-cyan flex items-center justify-center text-2xl mb-6 glow-blue">2</div>
                <h3 className="text-xl font-bold mb-2">Build</h3>
                <p className="text-gray-400">8 AI agents collaborate to design, source, and build.</p>
              </div>
              
              <div className="flex flex-col items-center">
                <div className="w-16 h-16 rounded-full bg-bg-dark border-2 border-brand-pink flex items-center justify-center text-2xl mb-6 shadow-[0_0_20px_rgba(236,72,153,0.5)]">3</div>
                <h3 className="text-xl font-bold mb-2">Launch</h3>
                <p className="text-gray-400">Your store goes live with products and payments.</p>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="w-full text-center py-8 text-gray-500 text-sm border-t border-white/10 mt-auto bg-black/60 relative z-10">
        AntiGravity © 2026 • Google Gemini XPRIZE
      </footer>
    </div>
  );
}
