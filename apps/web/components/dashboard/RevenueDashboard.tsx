'use client';

import { useBusinessStore } from '@/stores/businessStore';
import { motion } from 'framer-motion';

export function RevenueDashboard() {
  const { business } = useBusinessStore();
  
  // Calculate mock or real estimates
  const isLive = business?.status === 'live';
  const baseRevenue = isLive ? 12500 : 0;
  const startupCosts = isLive ? 450 : 0; // Domain, initial ad spend
  
  return (
    <div className="glass-card rounded-2xl p-6">
      <h2 className="text-xl font-display font-bold mb-6 flex items-center gap-2">
        <span>📈</span> Financial Projections
      </h2>
      
      <div className="space-y-4">
        <div className="bg-black/20 rounded-xl p-4 border border-white/5">
          <div className="text-gray-400 text-xs uppercase tracking-wider mb-1">Est. Year 1 Revenue</div>
          <div className="text-3xl font-bold text-green-400">
            ${isLive ? '150,000' : '---'}
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-black/20 rounded-xl p-4 border border-white/5">
            <div className="text-gray-400 text-xs uppercase tracking-wider mb-1">Startup Costs</div>
            <div className="text-xl font-bold text-red-400">
              ${isLive ? '450' : '---'}
            </div>
          </div>
          
          <div className="bg-black/20 rounded-xl p-4 border border-white/5">
            <div className="text-gray-400 text-xs uppercase tracking-wider mb-1">Profit Margin</div>
            <div className="text-xl font-bold text-brand-cyan">
              {isLive ? '68%' : '---'}
            </div>
          </div>
        </div>

        <div className="mt-4 text-xs font-pixel text-gray-500">
          Powered by Vault Agent AI Model
        </div>
      </div>
    </div>
  );
}
