import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "https://umarwaqar-full-stack-todo.hf.space",
});

export const { signIn, signUp, signOut, useSession } = authClient;
