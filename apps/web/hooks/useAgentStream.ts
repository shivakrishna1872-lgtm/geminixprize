import { useState, useEffect } from 'react';
import { AgentEvent } from '../types/events';

interface UseAgentStreamResult {
  events: AgentEvent[];
  isConnected: boolean;
  error: string | null;
}

export function useAgentStream(businessId: string | null): UseAgentStreamResult {
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!businessId) return;

    let eventSource: EventSource | null = null;
    let retryCount = 0;
    const maxRetries = 5;

    const connect = () => {
      eventSource = new EventSource(`/api/stream/${businessId}`);

      eventSource.onopen = () => {
        setIsConnected(true);
        setError(null);
        retryCount = 0;
      };

      eventSource.onmessage = (e) => {
        try {
          const data = JSON.parse(e.data);
          
          if (data.type === 'heartbeat') return;

          setEvents((prev) => {
            // Keep last 100 events to avoid memory issues
            const newEvents = [...prev, data as AgentEvent];
            if (newEvents.length > 100) return newEvents.slice(newEvents.length - 100);
            return newEvents;
          });
        } catch (err) {
          console.error('Error parsing SSE message:', err);
        }
      };

      eventSource.onerror = (e) => {
        console.error('SSE connection error:', e);
        setIsConnected(false);
        eventSource?.close();

        if (retryCount < maxRetries) {
          retryCount++;
          setTimeout(connect, Math.min(1000 * Math.pow(2, retryCount), 10000));
        } else {
          setError('Lost connection to orchestration server.');
        }
      };
    };

    connect();

    return () => {
      if (eventSource) {
        eventSource.close();
        setIsConnected(false);
      }
    };
  }, [businessId]);

  return { events, isConnected, error };
}
