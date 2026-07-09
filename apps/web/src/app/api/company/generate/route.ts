import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { companyBlueprintSchema } from "@antigravity/contracts";
import { z } from "zod";
import { authCookieName, geminiApiKeyCookieName } from "@/application/auth/session";
import { readServerWebEnv } from "@/infrastructure/config/web-env";

const generateRequestSchema = z.object({
  idea: z.string().min(8).max(800),
});

export async function POST(request: Request) {
  const env = readServerWebEnv();
  const sessionCookie = (await cookies()).get(authCookieName);
  const geminiApiKeyCookie = (await cookies()).get(geminiApiKeyCookieName);

  if (sessionCookie?.value !== env.APP_SESSION_TOKEN) {
    return NextResponse.json({ message: "Authentication required." }, { status: 401 });
  }

  const payload = generateRequestSchema.safeParse(await request.json());
  if (!payload.success) {
    return NextResponse.json({ message: "Enter a business idea with at least 8 characters." }, { status: 422 });
  }

  const upstreamResponse = await fetch(`${env.ANTIGRAVITY_API_BASE_URL}/v1/companies/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Antigravity-Api-Key": env.ANTIGRAVITY_INTERNAL_API_KEY,
      ...(geminiApiKeyCookie?.value ? { "X-Gemini-Api-Key": geminiApiKeyCookie.value } : {}),
    },
    body: JSON.stringify({ idea: payload.data.idea }),
    cache: "no-store",
  });

  if (!upstreamResponse.ok) {
    return NextResponse.json({ message: "Company generation failed upstream." }, { status: 502 });
  }

  const parsed = companyBlueprintSchema.safeParse(await upstreamResponse.json());
  if (!parsed.success) {
    return NextResponse.json({ message: "Company generation returned an invalid blueprint." }, { status: 502 });
  }

  return NextResponse.json(parsed.data);
}
