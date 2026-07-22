'use client';

import { useBusinessStore } from '@/stores/businessStore';
import { motion } from 'framer-motion';
import { AgentState } from '@/types/agent';

export function AgentGrid() {
  const { business } = useBusinessStore();
  const agents = business?.agents || {};
  
  // Enforce order based on DAG
  const agentOrder = ['atlas', 'nova', 'orbit', 'vault', 'forge', 'pulse', 'echo', 'insight'];
  
  return (
    <div className="glass-card rounded-2xl p-6">
      <h2 className="text-xl font-display font-bold mb-6 flex items-center gap-2">
        <span>🤖</span> Active Agents
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {agentOrder.map((id) => {
          const agent = agents[id] || { name: id, status: 'idle', progress: 0, emoji: '⚙️', logs: [] };
          return <AgentCard key={id} agent={agent as AgentState} />;
        })}
      </div>
    </div>
  );
}

function AgentCard({ agent }: { agent: AgentState }) {
  const isWorking = agent.status === 'working' || agent.status === 'thinking';
  const isDone = agent.status === 'done';
  const isError = agent.status === 'error';

  let borderColor = 'border-white/5';
  if (isWorking) borderColor = 'border-brand-purple/50 glow-purple';
  if (isDone) borderColor = 'border-green-500/30';
  if (isError) borderColor = 'border-red-500/50';

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-white/5 rounded-xl p-4 border ${borderColor} flex flex-col h-full`}
    >
      <div className="flex justify-between items-start mb-2">
        <div className="text-2xl">{agent.emoji}</div>
        <div className="text-[10px] font-pixel px-2 py-1 bg-black/40 rounded uppercase tracking-wider">
          {agent.status}
        </div>
      </div>
      
      <h3 className="font-display font-bold capitalize mt-1">{agent.name}</h3>
      <p className="text-xs text-brand-cyan mb-3">{agent.role}</p>
      
      <div className="mt-auto">
        <div className="text-xs text-gray-400 h-8 line-clamp-2 leading-tight mb-2">
          {agent.currentTask || 'Awaiting orders...'}
        </div>
        <div className="w-full bg-black/40 h-1.5 rounded-full overflow-hidden">
          <div 
            className={`h-full ${isDone ? 'bg-green-500' : isError ? 'bg-red-500' : 'bg-brand-purple'} transition-all duration-500`}
            style={{ width: `${agent.progress || 0}%` }}
          />
        </div>
      </div>
    </motion.div>
  );
}
