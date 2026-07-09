export const authCookieName = "antigravity_session";

export type AuthSession = Readonly<{
  authenticated: boolean;
}>;
