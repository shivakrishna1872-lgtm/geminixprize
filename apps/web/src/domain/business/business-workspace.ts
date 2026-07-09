export type BusinessWorkspace = Readonly<{
  id: string;
  name: string;
  operatingMode: "assisted" | "autonomous";
  createdAt: Date;
}>;
