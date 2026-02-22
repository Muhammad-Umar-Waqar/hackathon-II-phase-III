# Implementation Plan: AI Chat Agent & Conversation System

**Branch**: `1-ai-chat-agent` | **Date**: 2026-02-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-ai-chat-agent/spec.md`

## Summary

Implement a conversational AI interface for the Todo app using OpenAI Agents SDK. The system enables users to manage tasks through natural language by creating a stateless chat endpoint that rebuilds conversation context from the database on each request. The agent interprets user intent and suggests tool calls (add, list, update, complete, delete tasks) with confirmation prompts. This spec focuses on the conversation infrastructure and agent integration; MCP tool implementation is deferred to Spec-2.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/Next.js 14 (frontend)
**Primary Dependencies**: FastAPI 0.104+, OpenAI Agents SDK, SQLModel 0.0.14, Next.js 14, React 18
**Storage**: Neon PostgreSQL (existing connection via DATABASE_URL)
**Testing**: pytest 7.4+ (backend), Jest 29+ (frontend)
**Target Platform**: Linux server (backend), Web browser (frontend)
**Project Type**: Web application (existing backend/ and frontend/ structure)
**Performance Goals**: <3 seconds response time for chat messages, support 100+ concurrent conversations
**Constraints**: Stateless architecture (no in-memory session state), conversation context rebuilt from DB on each request, maintain Phase-II JWT authentication
**Scale/Scope**: Support existing user base with multiple concurrent conversations per user, conversation history up to 100 messages per conversation (MVP)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### VII. Agent-First Architecture ✅
- **Requirement**: Stateless agents that delegate all data operations to MCP tools
- **Compliance**: Chat endpoint is stateless; agent does not access database directly; conversation context rebuilt from DB on each request
- **Implementation**: Agent receives conversation history as input, returns tool call suggestions without executing them

### VIII. Conversation Persistence ✅
- **Requirement**: Persist all conversation state in database; rebuild context from DB on each request
- **Compliance**: Conversation and Message models store all chat history; context reconstruction logic in chat endpoint
- **Implementation**: Load conversation history from DB → format for agent → process message → persist new messages

### IX. Tool-Mediated Actions ✅
- **Requirement**: All task operations via MCP tools; tools are stateless and schema-defined
- **Compliance**: Agent suggests tool calls but does not execute them (execution in Spec-2); tool schemas defined for agent
- **Implementation**: Agent returns tool call suggestions (tool name + parameters); actual execution deferred to Spec-2

### X. AI Traceability ✅
- **Requirement**: Log all agent invocations with input prompts, tool calls, and responses
- **Compliance**: Existing logging infrastructure (src/utils/logger.py) extended for agent interactions
- **Implementation**: Log conversation_id, user_id, message content, agent response, tool calls, timestamps

### Phase-II Authentication ✅
- **Requirement**: Maintain JWT authentication and user isolation
- **Compliance**: Chat endpoint uses existing JWT verification (verify_token pattern from task_router.py)
- **Implementation**: Extract user_id from JWT; enforce conversation ownership; validate user can only access their conversations

### Rapid Prototyping ✅
- **Requirement**: MVP mindset, prioritize core features
- **Compliance**: Focus on P1 (start conversation) and P2 (resume conversation) for MVP; P3 (tool calls) demonstrates capability without full execution
- **Implementation**: Minimal viable chat interface; defer advanced features (streaming, pagination, conversation management)

**Gate Status**: ✅ PASSED - All constitution requirements satisfied

## Project Structure

### Documentation (this feature)

```text
specs/1-ai-chat-agent/
├── plan.md              # This file
├── research.md          # Phase 0 output (OpenAI Agents SDK, ChatKit, context management)
├── data-model.md        # Phase 1 output (Conversation, Message entities)
├── quickstart.md        # Phase 1 output (setup and testing guide)
├── contracts/           # Phase 1 output (chat API contract)
│   └── chat-api.yaml    # OpenAPI spec for chat endpoint
└── checklists/
    └── requirements.md  # Quality validation checklist
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py              # Existing
│   │   ├── user.py              # Existing
│   │   ├── conversation.py      # NEW: Conversation model
│   │   └── message.py           # NEW: Message model
│   ├── services/
│   │   ├── task_service.py      # Existing
│   │   ├── user_service.py      # Existing
│   │   ├── conversation_service.py  # NEW: Conversation CRUD
│   │   ├── message_service.py       # NEW: Message CRUD
│   │   └── agent_service.py         # NEW: OpenAI agent integration
│   ├── api/
│   │   ├── auth_router.py       # Existing
│   │   ├── task_router.py       # Existing
│   │   └── chat_router.py       # NEW: Chat endpoint
│   ├── utils/
│   │   ├── logger.py            # Existing (extend for agent logging)
│   │   └── context_builder.py   # NEW: Conversation context reconstruction
│   ├── database.py              # Existing
│   └── main.py                  # Existing (add chat_router)
└── tests/
    ├── test_conversation_service.py  # NEW
    ├── test_message_service.py       # NEW
    ├── test_agent_service.py         # NEW
    └── test_chat_router.py           # NEW

frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.tsx    # NEW: Main chat UI component
│   │   ├── MessageList.tsx      # NEW: Display conversation history
│   │   └── MessageInput.tsx     # NEW: User input field
│   ├── lib/
│   │   ├── auth-client.ts       # Existing
│   │   └── chat-client.ts       # NEW: API client for chat endpoint
│   └── types/
│       └── chat.ts              # NEW: TypeScript types for chat
└── pages/
    ├── chat.tsx                 # NEW: Chat page
    └── api/
        └── auth/[...all].ts     # Existing
```

**Structure Decision**: Web application structure (Option 2) selected. Existing backend/ and frontend/ directories maintained. New chat functionality integrated alongside existing task and auth modules. Backend follows service-layer pattern (models → services → routers). Frontend uses component-based architecture with API client abstraction.

## Complexity Tracking

> No constitution violations - this section is empty.

## Phase 0: Research & Technology Decisions

### Research Areas

1. **OpenAI Agents SDK Integration**
   - Decision: Use OpenAI Agents SDK for agent orchestration
   - Rationale: Required by Phase-III constraints; provides structured tool calling and conversation management
   - Alternatives considered: LangChain, custom OpenAI API integration
   - Implementation approach: Agent receives conversation history, returns response with tool call suggestions

2. **MCP SDK for Tool Definitions**
   - Decision: Define tool schemas using Official MCP SDK
   - Rationale: Required by Phase-III constraints; provides standardized tool interface
   - Alternatives considered: Custom tool schema definitions
   - Implementation approach: Define tool schemas (add_task, list_tasks, etc.) for agent; actual execution in Spec-2

3. **Conversation Context Management**
   - Decision: Rebuild full conversation context from database on each request
   - Rationale: Stateless architecture requirement; enables horizontal scaling
   - Alternatives considered: In-memory session cache (rejected - violates stateless principle)
   - Implementation approach: Load messages → format for agent → include in agent prompt

4. **ChatKit UI Library**
   - Decision: NEEDS CLARIFICATION - Determine if ChatKit is an existing library or custom component
   - Research needed: Investigate ChatKit availability, compatibility with Next.js/React
   - Fallback: Build custom chat UI components if ChatKit unavailable

5. **Agent Confirmation Pattern**
   - Decision: Agent asks for confirmation before suggesting destructive actions
   - Rationale: User safety and transparency (FR-009 requirement)
   - Implementation approach: Agent response includes confirmation prompt; user must explicitly approve

### Technology Stack Summary

**Backend:**
- FastAPI 0.104+ (existing)
- OpenAI Agents SDK (new dependency)
- Official MCP SDK (new dependency)
- SQLModel 0.0.14 (existing)
- PostgreSQL via Neon (existing)
- JWT authentication (existing)

**Frontend:**
- Next.js 14 (existing)
- React 18 (existing)
- ChatKit or custom chat components (to be determined)
- Axios for API calls (existing)

**Database Schema Extensions:**
- Conversation table (id, user_id, created_at, updated_at)
- Message table (id, conversation_id, user_id, role, content, created_at)

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for detailed entity definitions.

**Key Entities:**
- **Conversation**: Chat session between user and agent
- **Message**: Individual messages within a conversation (user/assistant/system roles)

### API Contracts

See [contracts/chat-api.yaml](./contracts/chat-api.yaml) for OpenAPI specification.

**Key Endpoint:**
- `POST /api/v1/chat` - Send message and receive agent response

### Quickstart Guide

See [quickstart.md](./quickstart.md) for setup and testing instructions.

## Implementation Phases

### Phase 0: Research ✅
- OpenAI Agents SDK integration patterns
- MCP SDK tool schema definitions
- Conversation context reconstruction strategies
- ChatKit UI library investigation

### Phase 1: Design ✅
- Data model for Conversation and Message entities
- API contract for chat endpoint
- Quickstart guide for development setup

### Phase 2: Implementation (via /sp.tasks)
- Database models and migrations
- Service layer (conversation, message, agent services)
- Chat API endpoint with JWT authentication
- Frontend chat UI components
- Integration testing

## Next Steps

1. Run `/sp.tasks` to generate implementation task breakdown
2. Review and approve task list
3. Execute tasks in dependency order
4. Test conversation flow end-to-end
5. Validate against success criteria (SC-001 through SC-010)
