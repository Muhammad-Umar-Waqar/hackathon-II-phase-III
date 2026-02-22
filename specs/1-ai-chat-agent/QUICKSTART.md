# Quickstart Guide: AI Chat Agent & Conversation System

**Feature**: 1-ai-chat-agent
**Date**: 2026-02-22
**Status**: ✅ Implementation Complete (54/54 tasks)
**Audience**: Developers testing and deploying this feature

## Implementation Status

✅ **All 54 tasks completed** across 6 phases:
- Phase 1: Setup (3 tasks) - Complete
- Phase 2: Foundational (4 tasks) - Complete
- Phase 3: User Story 1 - Start New Conversation (17 tasks) - Complete
- Phase 4: User Story 2 - Resume Existing Conversation (9 tasks) - Complete
- Phase 5: User Story 3 - Agent Tool Call Suggestions (11 tasks) - Complete
- Phase 6: Polish & Cross-Cutting Concerns (10 tasks) - Complete

**Ready for**: Manual testing, deployment, and integration with MCP tool execution (Spec-2)

**Action Required**: Update `OPENAI_API_KEY` in `backend/.env` with your actual OpenAI API key

## Quick Start Commands

**Get the system running in 5 steps:**

```bash
# 1. Update OpenAI API key in backend/.env
# Edit backend/.env and set: OPENAI_API_KEY=sk-your-actual-key

# 2. Apply database migrations
cd backend
alembic upgrade head

# 3. Start backend server (in one terminal)
cd backend
python -m uvicorn src.main:app --reload --port 8000

# 4. Start frontend server (in another terminal)
cd frontend
npm run dev

# 5. Open browser and test
# Navigate to: http://localhost:3000/chat
```

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ and npm installed
- PostgreSQL database (Neon) configured
- Phase-II authentication system operational
- Git repository cloned and on branch `1-ai-chat-agent`
- **OpenAI API key** (required for agent functionality)

## Environment Setup

### 1. Backend Dependencies

Add new dependencies to `backend/requirements.txt`:

```txt
# Existing dependencies remain...

# New dependencies for AI Chat Agent
openai>=1.0.0              # OpenAI SDK for agent integration
# Note: mcp-sdk not available in PyPI - using OpenAI native function calling format
```

Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Variables

Add to `backend/.env`:

```env
# Existing variables remain...

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=1000

# Chat Configuration
CHAT_RATE_LIMIT=30/minute
MAX_CONVERSATION_HISTORY=100
```

### 3. Database Migration

The migrations are already created in `backend/alembic/versions/`:
- `001_add_conversations.py` - Creates conversations table
- `002_add_messages.py` - Creates messages table

Apply the migrations:

```bash
cd backend
alembic upgrade head
```

Verify migrations applied:

```bash
alembic current
```

Expected output:
```
002_add_messages (head)
```

Verify tables created:

```sql
-- Connect to your Neon database
\dt conversations
\dt messages
```

Expected output:
```
 Schema |     Name       | Type  |  Owner
--------+----------------+-------+---------
 public | conversations  | table | neondb_owner
 public | messages       | table | neondb_owner
```

## Development Workflow

### 1. Start Backend Server

```bash
cd backend
python -m uvicorn src.main:app --reload --port 8000
```

Verify server is running:
```bash
curl http://localhost:8000/
# Expected: {"message": "Todo API is running", "status": "healthy", "version": "2.0"}
```

### 2. Start Frontend Development Server

```bash
cd frontend
npm run dev
```

Frontend should be available at `http://localhost:3000`

### 3. Test Authentication

Ensure Phase-II authentication is working:

```bash
# Register a test user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123", "name": "Test User"}'

# Login to get JWT token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'

# Save the token from response
export JWT_TOKEN="<token_from_response>"
```

## Testing the Chat API

### 1. Start New Conversation

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me my tasks"
  }'
```

Expected response:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message_id": "660e8400-e29b-41d4-a716-446655440001",
  "response": "You currently have 0 tasks. Would you like to add one?",
  "tool_calls": []
}
```

### 2. Continue Existing Conversation

```bash
# Use conversation_id from previous response
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Add a task to buy groceries"
  }'
```

Expected response:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message_id": "660e8400-e29b-41d4-a716-446655440002",
  "response": "I can add a task 'Buy groceries' for you. Would you like me to proceed?",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {
        "title": "Buy groceries"
      },
      "requires_confirmation": false
    }
  ]
}
```

### 3. Get Conversation History

```bash
curl -X GET "http://localhost:8000/api/v1/conversations/550e8400-e29b-41d4-a716-446655440000/messages" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

Expected response:
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user_123",
    "role": "user",
    "content": "Show me my tasks",
    "tool_calls": null,
    "created_at": "2026-02-22T10:30:00Z"
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440002",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user_123",
    "role": "assistant",
    "content": "You currently have 0 tasks. Would you like to add one?",
    "tool_calls": [],
    "created_at": "2026-02-22T10:30:05Z"
  }
]
```

## Frontend Integration

### 1. Test Chat UI

Navigate to `http://localhost:3000/chat` in your browser.

Expected behavior:
- Chat interface loads with empty message list
- User can type message in input field
- Clicking "Send" sends message to backend
- Agent response appears in message list
- Conversation persists across page refreshes

### 2. Manual Testing Checklist

- [ ] User can start a new conversation
- [ ] User can send messages and receive responses
- [ ] Agent correctly interprets task-related commands
- [ ] Tool call suggestions appear in responses
- [ ] Conversation history loads correctly
- [ ] User can only access their own conversations
- [ ] Error messages display for invalid inputs
- [ ] Rate limiting works (30 requests/minute)

## Running Tests

### Backend Unit Tests

```bash
cd backend
pytest tests/test_conversation_service.py -v
pytest tests/test_message_service.py -v
pytest tests/test_agent_service.py -v
pytest tests/test_chat_router.py -v
```

### Backend Integration Tests

```bash
cd backend
pytest tests/integration/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Debugging

### Enable Debug Logging

Add to `backend/.env`:
```env
LOG_LEVEL=DEBUG
```

Restart backend server to see detailed logs.

### Common Issues

**Issue**: "OpenAI API key not found"
- **Solution**: Ensure `OPENAI_API_KEY` is set in `backend/.env`

**Issue**: "Conversation not found"
- **Solution**: Verify conversation_id is correct and belongs to authenticated user

**Issue**: "Rate limit exceeded"
- **Solution**: Wait 1 minute or adjust `CHAT_RATE_LIMIT` in `.env`

**Issue**: "Agent response timeout"
- **Solution**: Check OpenAI API status, increase timeout in agent service

**Issue**: "Database connection error"
- **Solution**: Verify `DATABASE_URL` is correct and Neon database is accessible

### Viewing Logs

Backend logs:
```bash
tail -f backend/backend.log
```

Frontend logs:
```bash
# Check browser console (F12)
```

## Performance Monitoring

### Response Time Metrics

Monitor chat endpoint response times:

```bash
# Check logs for timing information
grep "Request completed.*chat" backend/backend.log | tail -20
```

Target: <3 seconds per request

### Database Query Performance

Check slow queries:

```sql
-- Connect to Neon database
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE query LIKE '%conversations%' OR query LIKE '%messages%'
ORDER BY mean_exec_time DESC
LIMIT 10;
```

## Next Steps

### Current Status: Implementation Complete ✅

All 54 tasks have been completed. The system is ready for testing and deployment.

### Immediate Actions Required

1. **Update OpenAI API Key**
   ```bash
   # Edit backend/.env and replace placeholder with your actual key
   OPENAI_API_KEY=sk-your-actual-openai-api-key-here
   ```

2. **Verify Database Migrations**
   ```bash
   cd backend
   alembic current
   # Should show: 002_add_messages (head)
   ```

3. **Start Testing**
   - Follow the "Testing the Chat API" section above
   - Complete the "Manual Testing Checklist"
   - Verify all 3 user stories work independently

### Testing Workflow

1. ✅ Environment setup complete
2. ✅ Database migrations applied
3. ✅ All backend services implemented
4. ✅ All frontend components implemented
5. → **Update OPENAI_API_KEY** (required before testing)
6. → Start backend and frontend servers
7. → Run manual tests for all 3 user stories
8. → Verify rate limiting (30 requests/minute)
9. → Verify user isolation
10. → Test conversation context rebuilding

### Future Enhancements (Spec-2)

- MCP server setup for tool execution
- Implement actual task CRUD operations via MCP tools
- Connect tool calls to real task database operations
- Add automated tests (unit, integration, E2E)

## Reference Documentation

- [Feature Spec](./spec.md) - Requirements and user stories
- [Implementation Plan](./plan.md) - Architecture and design decisions
- [Data Model](./data-model.md) - Database schema and entities
- [API Contract](./contracts/chat-api.yaml) - OpenAPI specification
- [Research](./research.md) - Technology decisions and best practices

## Support

For issues or questions:
1. Check logs for error messages
2. Review [research.md](./research.md) for common patterns
3. Consult [data-model.md](./data-model.md) for database schema
4. Refer to [chat-api.yaml](./contracts/chat-api.yaml) for API contract
