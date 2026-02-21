const { betterAuth } = require('better-auth');
const { Pool } = require('pg');
require('dotenv').config({ path: '.env.local' });

async function testBetterAuth() {
  console.log('Testing Better Auth directly...\n');

  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
  });

  const auth = betterAuth({
    database: pool,
    emailAndPassword: {
      enabled: true,
      requireEmailVerification: false,
    },
    secret: process.env.BETTER_AUTH_SECRET,
    trustedOrigins: ["http://localhost:3000"],
    baseURL: "http://localhost:3000",
  });

  console.log('✓ Better Auth initialized');
  console.log('✓ Handler exists:', typeof auth.handler);

  // Test the handler with a mock request
  const testRequest = new Request('http://localhost:3000/api/auth/sign-up/email', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: 'directtest@example.com',
      password: 'Password123',
      name: 'Direct Test'
    })
  });

  console.log('\nTesting sign-up request...');

  try {
    const response = await auth.handler(testRequest);
    const data = await response.text();

    console.log('Response status:', response.status);
    console.log('Response body:', data);

    if (response.status === 200 || response.status === 201) {
      console.log('\n✓ Better Auth is working correctly!');
    } else {
      console.log('\n✗ Better Auth returned error:', response.status);
    }
  } catch (error) {
    console.error('\n✗ Better Auth handler failed:', error.message);
    console.error('Stack:', error.stack);
  }

  await pool.end();
}

testBetterAuth().catch(console.error);
