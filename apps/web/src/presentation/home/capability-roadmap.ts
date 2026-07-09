type CapabilityRoadmapItem = Readonly<{
  name: string;
  stage: "Foundation" | "MVP" | "Future";
  description: string;
}>;

export const capabilityRoadmap: readonly CapabilityRoadmapItem[] = [
  {
    name: "Market Intelligence",
    stage: "Future",
    description:
      "Research agents will identify market signals, customer segments, and demand patterns before product decisions are made.",
  },
  {
    name: "Business Strategy",
    stage: "MVP",
    description:
      "Strategy agents will convert a business idea into positioning, launch priorities, risk notes, and execution plans.",
  },
  {
    name: "Product Operations",
    stage: "MVP",
    description:
      "Product agents will generate validated commerce-ready drafts with copy, pricing, category, tags, and review state.",
  },
  {
    name: "Launch Systems",
    stage: "Future",
    description:
      "Launch agents will prepare storefronts, marketing assets, channel plans, and performance analysis workflows.",
  },
];
