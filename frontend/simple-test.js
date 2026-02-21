// Minimal test to see what's happening
const http = require('http');

const data = JSON.stringify({
  email: `test${Date.now()}@example.com`,
  password: 'Password123!',
  name: 'Test'
});

const options = {
  hostname: 'localhost',
  port: 3000,
  path: '/api/auth/sign-up/email',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length
  }
};

const req = http.request(options, (res) => {
  console.log(`Status: ${res.statusCode}`);
  console.log(`Headers: ${JSON.stringify(res.headers)}`);
  
  let body = '';
  res.on('data', (chunk) => { body += chunk; });
  res.on('end', () => {
    console.log(`Body: ${body}`);
    if (body) {
      try {
        console.log('Parsed:', JSON.parse(body));
      } catch (e) {
        console.log('Not JSON');
      }
    }
  });
});

req.on('error', (e) => {
  console.error(`Error: ${e.message}`);
});

req.write(data);
req.end();
