'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { useBusinessStore } from '@/stores/businessStore';
import { useAgentStream } from '@/hooks/useAgentStream';
import { AgentGrid } from '@/components/dashboard/AgentGrid';
import { WebsitePreview } from '@/components/dashboard/WebsitePreview';
import { RevenueDashboard } from '@/components/dashboard/RevenueDashboard';

export default function DashboardPage() {
  const params = useParams();
  const id = params.id as string;
  const { business, setBusiness, applyEvent } = useBusinessStore();
  const { events, isConnected } = useAgentStream(id);
  const [loading, setLoading] = useState(true);

  // Fetch initial business state
  useEffect(() => {
    let isMounted = true;
    const fetchBusiness = async () => {
      try {
        const res = await fetch(`/api/business/${id}`, {
          headers: { 'Authorization': 'Bearer mock-token' }
        });
        if (res.ok) {
          const data = await res.json();
          if (isMounted) setBusiness(data);
        }
      } catch (e) {
        console.error('Failed to fetch business', e);
      } finally {
        if (isMounted) setLoading(false);
      }
    };
    fetchBusiness();
    return () => { isMounted = false; };
  }, [id, setBusiness]);

  // Apply SSE events to the store
  useEffect(() => {
    if (events.length > 0) {
      // Apply the most recent event to the store
      applyEvent(events[events.length - 1]);
    }
  }, [events, applyEvent]);

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center font-pixel">Initializing Mission Control...</div>;
  }

  return (
    <div className="min-h-screen bg-bg-dark text-white p-6 md:p-12 overflow-x-hidden">
      <header className="flex justify-between items-center mb-8 border-b border-white/10 pb-6">
        <div>
          <h1 className="text-3xl font-display font-bold gradient-text">Mission Control</h1>
          <p className="text-gray-400 font-pixel text-sm mt-2">
            ID: {id} | STATUS: {business?.status?.toUpperCase()}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-sm text-gray-400 font-pixel">Uplink:</div>
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500 glow-blue animate-pulse' : 'bg-red-500'}`} />
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          <AgentGrid />
          <WebsitePreview />
        </div>
        <div className="space-y-8">
          <RevenueDashboard />
          
          <div className="glass-card rounded-2xl p-6">
            <h2 className="text-xl font-display font-bold mb-4 flex items-center gap-2">
              <span>📡</span> Live Feed
            </h2>
            <div className="h-64 overflow-y-auto font-pixel text-xs space-y-2 scrollbar-hide">
              {events.slice(-50).reverse().map((ev, i) => (
                <div key={i} className="border-l-2 border-brand-purple pl-2 py-1">
                  <span className="text-brand-pink opacity-70">[{ev.agentId?.toUpperCase() || 'SYS'}]</span>{' '}
                  <span className="text-gray-300">{ev.logLine || ev.task || ev.eventType}</span>
                </div>
              ))}
              {events.length === 0 && <div className="text-gray-500">Waiting for signals...</div>}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
