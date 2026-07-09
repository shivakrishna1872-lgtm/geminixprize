import { NextResponse } from "next/server";
import { z } from "zod";
import { authCookieName } from "@/application/auth/session";
import { readServerWebEnv } from "@/infrastructure/config/web-env";

const loginRequestSchema = z.object({
  password: z.string().min(1),
});

export async function POST(request: Request) {
  const env = readServerWebEnv();
  const payload = loginRequestSchema.safeParse(await request.json());

  if (!payload.success || payload.data.password !== env.APP_AUTH_PASSWORD) {
    return NextResponse.json({ message: "Invalid passcode." }, { status: 401 });
  }

  const response = NextResponse.json({ authenticated: true });
  response.cookies.set({
    name: authCookieName,
    value: env.APP_SESSION_TOKEN,
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
  });

  return response;
}
