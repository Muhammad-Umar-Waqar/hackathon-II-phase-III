#!/bin/bash
echo "=================================="
echo "Verifying Better Auth Setup"
echo "=================================="
echo ""

# Check Pages Router auth file
if [ -f "pages/api/auth/[...all].ts" ]; then
    echo "✓ Pages Router auth file exists"
else
    echo "✗ Pages Router auth file MISSING"
    exit 1
fi

# Check lib files
if [ -f "lib/auth.ts" ]; then
    echo "✓ lib/auth.ts exists"
else
    echo "✗ lib/auth.ts MISSING"
    exit 1
fi

if [ -f "lib/auth-client.ts" ]; then
    echo "✓ lib/auth-client.ts exists"
else
    echo "✗ lib/auth-client.ts MISSING"
    exit 1
fi

# Check .env.local
if [ -f ".env.local" ]; then
    echo "✓ .env.local exists"
    if grep -q "DATABASE_URL" .env.local; then
        echo "  ✓ DATABASE_URL is set"
    else
        echo "  ✗ DATABASE_URL is MISSING"
    fi
    if grep -q "BETTER_AUTH_SECRET" .env.local; then
        echo "  ✓ BETTER_AUTH_SECRET is set"
    else
        echo "  ✗ BETTER_AUTH_SECRET is MISSING"
    fi
else
    echo "✗ .env.local MISSING"
    exit 1
fi

# Check App Router auth is removed
if [ -d "src/app/api/auth" ]; then
    echo "✗ App Router auth directory still exists (should be removed)"
    exit 1
else
    echo "✓ App Router auth removed"
fi

# Check cache is clean
if [ -d ".next" ]; then
    echo "⚠ .next directory exists (will be rebuilt on start)"
else
    echo "✓ .next cache is clean"
fi

echo ""
echo "=================================="
echo "✓ Setup verification PASSED"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Run: npm run dev"
echo "2. Wait for: ✓ Ready in X ms"
echo "3. Test: curl -X POST http://localhost:3000/api/auth/sign-up/email -H 'Content-Type: application/json' -d '{\"email\":\"test@example.com\",\"password\":\"Password123!\",\"name\":\"Test\"}'"
echo ""
