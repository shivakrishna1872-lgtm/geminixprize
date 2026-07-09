export const authCookieName = "antigravity_session";
export const geminiApiKeyCookieName = "madethis_gemini_api_key";
export const openaiApiKeyCookieName = "madethis_openai_api_key";

export type AuthSession = Readonly<{
  authenticated: boolean;
}>;
