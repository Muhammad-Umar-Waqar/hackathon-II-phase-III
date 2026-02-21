require('dotenv').config({ path: '.env.local' });
const { Pool } = require('pg');
const fs = require('fs');

async function fixSchema() {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  
  console.log('Dropping existing Better Auth tables...');
  
  try {
    await pool.query('DROP TABLE IF EXISTS verification CASCADE');
    await pool.query('DROP TABLE IF EXISTS session CASCADE');
    await pool.query('DROP TABLE IF EXISTS account CASCADE');
    await pool.query('DROP TABLE IF EXISTS "user" CASCADE');
    
    console.log('✓ Tables dropped');
    console.log('\nBetter Auth will auto-create tables with correct schema on next request.');
    
  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await pool.end();
  }
}

fixSchema();
