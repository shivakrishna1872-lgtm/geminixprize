import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { z } from "zod";
import {
  authCookieName,
  geminiApiKeyCookieName,
  openaiApiKeyCookieName,
} from "@/application/auth/session";
import { readServerWebEnv } from "@/infrastructure/config/web-env";

const secretsRequestSchema = z.object({
  geminiApiKey: z.string().min(1).optional(),
  openaiApiKey: z.string().min(1).optional(),
});

export async function POST(request: Request) {
  const env = readServerWebEnv();
  const cookieStore = await cookies();
  const sessionCookie = cookieStore.get(authCookieName);

  if (sessionCookie?.value !== env.APP_SESSION_TOKEN) {
    return NextResponse.json({ message: "Authentication required." }, { status: 401 });
  }

  const payload = secretsRequestSchema.safeParse(await request.json());
  if (!payload.success) {
    return NextResponse.json({ message: "Invalid secret payload." }, { status: 422 });
  }

  const response = NextResponse.json({ configured: Boolean(payload.data.geminiApiKey) });
  const cookieOptions = {
    httpOnly: true,
    sameSite: "lax" as const,
    secure: process.env.NODE_ENV === "production",
    path: "/",
  };

  if (payload.data.geminiApiKey) {
    response.cookies.set({
      ...cookieOptions,
      name: geminiApiKeyCookieName,
      value: payload.data.geminiApiKey,
    });
  }

  if (payload.data.openaiApiKey) {
    response.cookies.set({
      ...cookieOptions,
      name: openaiApiKeyCookieName,
      value: payload.data.openaiApiKey,
    });
  }

  return response;
}
