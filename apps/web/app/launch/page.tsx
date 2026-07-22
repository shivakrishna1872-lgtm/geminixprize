"use client";

import { useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion } from "framer-motion";

function LaunchContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const prompt = searchParams.get("prompt") || "Building your business...";
  const [dots, setDots] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? "" : prev + "."));
    }, 500);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (!prompt) return;

    let isMounted = true;
    const launchBusiness = async () => {
      try {
        const res = await fetch("/api/launch", {
          method: "POST",
          headers: { "Content-Type": "application/json", "Authorization": "Bearer mock-token" },
          body: JSON.stringify({ prompt }),
        });
        
        if (!res.ok) throw new Error("Failed to launch business");
        
        const data = await res.json();
        if (isMounted && data.business_id) {
          router.push(`/dashboard/${data.business_id}`);
        }
      } catch (err) {
        if (isMounted) setError(err instanceof Error ? err.message : "An error occurred");
      }
    };

    launchBusiness();
    
    return () => { isMounted = false; };
  }, [prompt, router]);

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-card p-12 rounded-3xl max-w-2xl w-full text-center"
    >
      <div className="text-6xl mb-6 animate-float">🧠</div>
      <h1 className="text-3xl md:text-4xl font-display font-bold mb-4">
        {error ? "Launch Failed" : `Atlas is analyzing your idea${dots}`}
      </h1>
      <p className={`text-lg mb-8 font-pixel ${error ? "text-red-400" : "text-gray-400"}`}>
        &gt; {error || prompt}
      </p>
      
      {!error && (
        <>
          <div className="w-full bg-black/50 h-2 rounded-full overflow-hidden">
            <div className="h-full bg-brand-purple w-1/3 animate-pulse" />
          </div>
          <p className="mt-8 text-sm text-brand-cyan uppercase tracking-widest glow-blue inline-block">
            Orchestration Initiated
          </p>
        </>
      )}
    </motion.div>
  );
}

export default function LaunchPage() {
  return (
    <div className="min-h-screen bg-bg-dark flex flex-col items-center justify-center p-6">
      <Suspense fallback={<div>Loading...</div>}>
        <LaunchContent />
      </Suspense>
    </div>
  );
}
