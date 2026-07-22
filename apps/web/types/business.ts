/**
 * Business domain types for AntiGravity.
 * Represents the full state of an AI-generated business.
 */

import { AgentState } from './agent';

export interface BrandIdentity {
  name: string;
  tagline: string;
  primaryColor: string;
  secondaryColor: string;
  accentColor: string;
  fontHeading: string;
  fontBody: string;
  logoUrl?: string;
  styleKeywords: string[];
}

export interface Product {
  id: string;
  name: string;
  description: string;
  priceUsd: number;
  imageUrl?: string;
  tags: string[];
}

export interface BusinessBlueprint {
  niche: string;
  target_audience: string;
  value_proposition: string;
  competitors: string[];
  pricing_strategy: string;
  revenue_model: string;
  launch_checklist: string[];
}

export interface Business {
  id: string;
  prompt: string;
  status: 'queued' | 'running' | 'live' | 'failed';
  blueprint?: BusinessBlueprint;
  brand?: BrandIdentity;
  products: Product[];
  websiteUrl?: string;
  agents: Record<string, AgentState>;
  createdAt: string;
}
