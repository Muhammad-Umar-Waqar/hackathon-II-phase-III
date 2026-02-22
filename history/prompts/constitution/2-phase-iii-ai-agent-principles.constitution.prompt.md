---
id: 2
title: Phase-III AI Agent Principles
stage: constitution
date: 2026-02-22
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "phase-iii", "ai-agents", "architecture", "mcp-tools"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

/sp.constitution (Phase-III Update)

Project Extension: AI-Powered Todo Chatbot

Core additions:
- Agent-first design using OpenAI Agents SDK
- Stateless chat and tool execution
- All task actions executed only via MCP tools
- Clear separation: UI → Agent → MCP Tools → Database

Key standards:
- Agents must not access the database directly
- MCP tools must be stateless and schema-defined
- Conversation context rebuilt from database each request
- All AI actions traceable and persisted
- Phase-II auth and user isolation rules remain enforced

Constraints:
- Use OpenAI Agents SDK and Official MCP SDK
- Stateless FastAPI chat endpoint
- Persist conversations and messages in Neon PostgreSQL
- No manual coding; Claude Code only

Success criteria:
- Users manage todos via natural language
- Agent correctly invokes MCP tools
- Conversation resumes after restart
- System remains secure and stateless

## Response snapshot

Updated constitution from version 1.0.0 to 1.1.0 (MINOR bump) by adding four new principles for Phase-III AI-Powered Todo Chatbot:

**New Principles Added:**
- VII. Agent-First Architecture: Stateless agents that delegate all data operations to MCP tools
- VIII. Conversation Persistence: Database-backed conversation state for resumption
- IX. Tool-Mediated Actions: All task operations via MCP tools with schema validation
- X. AI Traceability: Comprehensive logging of agent invocations and tool executions

**New Constraints Section:**
- Phase-III Constraints: OpenAI Agents SDK, MCP SDK, stateless FastAPI, Neon PostgreSQL
- Natural Language Interface requirements
- Security and Isolation rules (Phase-II guarantees maintained)

**Testing Strategy Updated:**
- Added agent-tool interaction testing requirements
- Added conversation persistence validation scenarios

All existing principles (I-VI) and Phase-II constraints preserved. Templates reviewed and confirmed compatible.

## Outcome

- ✅ Impact: Constitution extended with AI agent architecture principles; version bumped 1.0.0 → 1.1.0
- 🧪 Tests: No tests (documentation update)
- 📁 Files: Modified .specify/memory/constitution.md
- 🔁 Next prompts: /sp.specify for Phase-III feature spec, /sp.plan for architecture design
- 🧠 Reflection: MINOR version bump appropriate (additive changes, no breaking modifications to existing principles)

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual validation - PASS (all placeholders filled, version incremented correctly, sync impact report complete)
- Prompt variant (if applicable): Standard constitution update workflow
- Next experiment (smallest change to try): N/A
