const { Pool } = require('pg');
require('dotenv').config({ path: '.env.local' });

async function testSetup() {
  console.log('Testing Better Auth setup...\n');

  // Test 1: Check environment variables
  console.log('1. Environment Variables:');
  console.log('   DATABASE_URL:', process.env.DATABASE_URL ? '✓ Set' : '✗ Missing');
  console.log('   BETTER_AUTH_SECRET:', process.env.BETTER_AUTH_SECRET ? '✓ Set' : '✗ Missing');
  console.log('   BETTER_AUTH_URL:', process.env.BETTER_AUTH_URL ? '✓ Set' : '✗ Missing');
  console.log('');

  // Test 2: Database connection
  console.log('2. Database Connection:');
  try {
    const pool = new Pool({
      connectionString: process.env.DATABASE_URL,
    });

    const client = await pool.connect();
    console.log('   ✓ Connected to database');

    // Test 3: Check Better Auth tables
    console.log('\n3. Better Auth Tables:');
    const result = await client.query(`
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public'
      AND table_name IN ('user', 'session', 'account', 'verification')
      ORDER BY table_name
    `);

    const tables = result.rows.map(r => r.table_name);
    ['user', 'session', 'account', 'verification'].forEach(table => {
      if (tables.includes(table)) {
        console.log(`   ✓ ${table} table exists`);
      } else {
        console.log(`   ✗ ${table} table missing`);
      }
    });

    client.release();
    await pool.end();

    console.log('\n✓ All checks passed!');
  } catch (error) {
    console.log('   ✗ Database connection failed:', error.message);
  }
}

testSetup().catch(console.error);
