#!/bin/bash
echo "Switching to Pages Router for Better Auth..."

# Remove App Router auth
rm -rf src/app/api/auth

# Pages Router file already created at pages/api/auth/[...all].ts

# Clean cache
rm -rf .next
rm -rf node_modules/.cache

echo "Done! Now run: npm run dev"
