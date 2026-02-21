import { betterAuth } from "better-auth";
import { Pool } from "pg";

// Database connection for Better Auth
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export const auth = betterAuth({
  database: {
    provider: "pg",
    pool,
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
  jwt: {
    enabled: true,
    secret: process.env.BETTER_AUTH_SECRET || process.env.JWT_SECRET,
    expiresIn: 60 * 30, // 30 minutes
  },
  trustedOrigins: [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://hackathon-ii-phase-ii-giaic.vercel.app",
  ],
});

export type Session = typeof auth.$Infer.Session;
