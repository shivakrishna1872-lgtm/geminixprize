export type BusinessType = Readonly<{
  label: string;
  icon: string;
}>;

export type AgentCard = Readonly<{
  name: string;
  role: string;
  output: string;
}>;

export type PricingPlan = Readonly<{
  name: string;
  price: string;
  summary: string;
  highlights: readonly string[];
  featured?: boolean;
}>;

export const businessTypes: readonly BusinessType[] = [
  { label: "Dropshipping brand", icon: "box" },
  { label: "Marketing agency", icon: "megaphone" },
  { label: "Online course", icon: "book" },
  { label: "SaaS product", icon: "terminal" },
  { label: "Clothing label", icon: "shirt" },
  { label: "Photo studio", icon: "camera" },
  { label: "Service business", icon: "briefcase" },
  { label: "Furniture store", icon: "chair" },
];

export const agents: readonly AgentCard[] = [
  {
    name: "CEO",
    role: "Strategy command",
    output: "Turns the founder prompt into a company operating plan.",
  },
  {
    name: "Research",
    role: "Market radar",
    output: "Studies segments, competitors, positioning, and demand signals.",
  },
  {
    name: "Branding",
    role: "Identity studio",
    output: "Creates names, voice, visual direction, and launch messaging.",
  },
  {
    name: "Product",
    role: "Offer factory",
    output: "Generates products, listings, pricing, bundles, and assets.",
  },
  {
    name: "Store",
    role: "Commerce launch",
    output: "Prepares storefront structure, checkout, catalog, and deployment.",
  },
  {
    name: "Marketing",
    role: "Growth engine",
    output: "Builds SEO, email, ads, launch calendars, and campaign copy.",
  },
];

export const pricingPlans: readonly PricingPlan[] = [
  {
    name: "Starter",
    price: "$49/mo",
    summary: "For early founders launching one autonomous business.",
    highlights: ["1 business", "5,000 credits/month", "Subdomain hosting", "Basic support"],
  },
  {
    name: "Growth",
    price: "$79/mo",
    summary: "For builders ready to run multiple AI-assisted ventures.",
    highlights: ["3 businesses", "10,000 credits/month", "Custom domain", "Priority support"],
    featured: true,
  },
  {
    name: "Scale",
    price: "$199/mo",
    summary: "For operators scaling a portfolio of autonomous businesses.",
    highlights: ["10 businesses", "30,000 credits/month", "Custom domain", "Dedicated support"],
  },
];
