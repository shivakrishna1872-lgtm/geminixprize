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

export interface Business {
  id: string;
  prompt: string;
  status: 'queued' | 'running' | 'live' | 'failed';
  brand?: BrandIdentity;
  products: Product[];
  websiteUrl?: string;
  agents: Record<string, AgentState>;
  createdAt: string;
}
