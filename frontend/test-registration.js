const fetch = require('node-fetch');

async function testRegistration() {
  console.log('Testing Better Auth registration...\n');
  
  const email = `test${Date.now()}@example.com`;
  const data = {
    email: email,
    password: 'Password123!',
    name: 'Test User'
  };
  
  console.log('Request:', JSON.stringify(data, null, 2));
  
  try {
    const response = await fetch('http://localhost:3000/api/auth/sign-up/email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    
    console.log('\nStatus:', response.status);
    console.log('Headers:', Object.fromEntries(response.headers.entries()));
    
    const text = await response.text();
    console.log('\nResponse body:', text);
    
    if (text) {
      try {
        const json = JSON.parse(text);
        console.log('\nParsed JSON:', JSON.stringify(json, null, 2));
        
        if (json.user) {
          console.log('\n✓ SUCCESS! User created:', json.user.email);
        } else if (json.error) {
          console.log('\n✗ ERROR:', json.error);
        }
      } catch (e) {
        console.log('\n✗ Response is not JSON');
      }
    } else {
      console.log('\n✗ Empty response');
    }
  } catch (error) {
    console.error('\n✗ Request failed:', error.message);
  }
}

testRegistration();
