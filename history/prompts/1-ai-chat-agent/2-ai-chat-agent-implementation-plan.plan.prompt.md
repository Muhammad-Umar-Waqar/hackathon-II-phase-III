---
id: 2
title: AI Chat Agent Implementation Plan
stage: plan
date: 2026-02-22
surface: agent
model: claude-sonnet-4-6
feature: 1-ai-chat-agent
branch: 1-ai-chat-agent
user: user
command: /sp.plan
labels: ["plan", "architecture", "openai-agents-sdk", "conversation-system", "mcp-tools"]
links:
  spec: specs/1-ai-chat-agent/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-chat-agent/plan.md
  - specs/1-ai-chat-agent/research.md
  - specs/1-ai-chat-agent/data-model.md
  - specs/1-ai-chat-agent/contracts/chat-api.yaml
  - specs/1-ai-chat-agent/quickstart.md
  - CLAUDE.md
tests:
  - none
---

## Prompt

before planning first you can review the frontend and backend folders, after that generate plan. here is plan /sp.plan
/sp.plan (Spec-1 — AI Chat Agent & Conversation System)

1. Setup FastAPI backend & Neon DB
2. Create Conversation & Message models
3. Implement POST /api/{user_id}/chat
4. Integrate OpenAI Agent (map messages → tool calls)
5. Rebuild conversation context per request (stateless)
6. Connect ChatKit UI to backend
7. Test chat flow, confirmations, error handling

## Response snapshot

Generated comprehensive implementation plan for AI Chat Agent & Conversation System after reviewing existing backend (FastAPI, SQLModel, JWT auth) and frontend (Next.js 14, React 18) architecture.

**Plan Structure**:
- Technical Context: Python 3.11+, FastAPI, OpenAI Agents SDK, MCP SDK, Neon PostgreSQL, Next.js 14
- Constitution Check: ✅ All principles validated (Agent-First Architecture, Conversation Persistence, Tool-Mediated Actions, AI Traceability, Phase-II Auth)
- Project Structure: Web application (backend/ and frontend/ directories maintained)

**Phase 0: Research (research.md)**:
- OpenAI Agents SDK integration patterns (stateless operation with conversation history)
- MCP SDK tool schema definitions (add_task, list_tasks, update_task, complete_task, delete_task)
- Conversation context reconstruction (load from DB, format for agent, limit 100 messages)
- ChatKit investigation (build custom components - no existing library found)
- Agent confirmation pattern (two-step flow for destructive actions)

**Phase 1: Design**:

1. **Data Model (data-model.md)**:
   - Conversation entity: id, user_id, created_at, updated_at
   - Message entity: id, conversation_id, user_id, role, content, tool_calls, created_at
   - Indexes: (user_id), (conversation_id, created_at)
   - Migration script with foreign keys and constraints

2. **API Contract (contracts/chat-api.yaml)**:
   - POST /api/v1/chat - Send message, receive agent response
   - GET /api/v1/conversations - List user's conversations
   - GET /api/v1/conversations/{id}/messages - Get conversation history
   - JWT authentication, rate limiting (30/minute), error responses

3. **Quickstart Guide (quickstart.md)**:
   - Environment setup (OpenAI API key, dependencies)
   - Database migration steps
   - Testing procedures (curl examples)
   - Debugging tips and performance monitoring

**Architecture Decisions**:
- Stateless chat endpoint (rebuild context from DB on each request)
- Agent suggests tool calls but doesn't execute them (execution in Spec-2)
- JWT authentication pattern from existing task_router.py
- Service layer pattern: models → services → routers
- Custom chat UI components (ChatInterface, MessageList, MessageInput)

**Agent Context Updated**: Added OpenAI Agents SDK, MCP SDK to CLAUDE.md

**Ready for**: /sp.tasks to generate implementation task breakdown

## Outcome

- ✅ Impact: Complete implementation plan with research, data model, API contract, and quickstart guide
- 🧪 Tests: No tests (planning phase)
- 📁 Files: Created plan.md, research.md, data-model.md, chat-api.yaml, quickstart.md; updated CLAUDE.md
- 🔁 Next prompts: /sp.tasks for task breakdown, then implementation execution
- 🧠 Reflection: Plan maintains stateless architecture (constitution principle VII), integrates with existing FastAPI/Next.js structure, defers MCP tool execution to Spec-2 for clean separation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check validation - PASS (all 6 principles satisfied)
- Prompt variant (if applicable): Standard planning workflow with architecture review
- Next experiment (smallest change to try): N/A
