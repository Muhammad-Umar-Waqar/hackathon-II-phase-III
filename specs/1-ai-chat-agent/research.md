# Research: AI Chat Agent & Conversation System

**Feature**: 1-ai-chat-agent
**Date**: 2026-02-22
**Status**: Complete

## Research Questions

### 1. OpenAI Agents SDK Integration

**Question**: How to integrate OpenAI Agents SDK for stateless conversation processing?

**Research Findings**:
- OpenAI Agents SDK provides structured agent orchestration with tool calling capabilities
- Agents can be configured with system prompts, tool definitions, and conversation history
- SDK supports stateless operation by accepting conversation history as input parameter
- Agent responses include text content and structured tool call suggestions

**Decision**: Use OpenAI Agents SDK with conversation history passed on each request

**Rationale**:
- Required by Phase-III constraints
- Provides built-in tool calling framework
- Supports stateless architecture (no session management required)
- Well-documented and actively maintained

**Implementation Approach**:
```python
# Pseudocode
agent = Agent(
    model="gpt-4",
    system_prompt="You are a helpful todo assistant...",
    tools=[add_task_tool, list_tasks_tool, ...]
)

# On each request
response = agent.run(
    messages=conversation_history,  # Loaded from DB
    new_message=user_message
)
```

**Alternatives Considered**:
- LangChain: More complex, heavier framework
- Custom OpenAI API integration: More control but requires building tool calling logic
- Anthropic Claude: Different API, would require significant changes

### 2. MCP SDK Tool Schema Definitions

**Question**: How to define tool schemas for the agent using Official MCP SDK?

**Research Findings**:
- MCP SDK provides standardized schema format for tool definitions
- Tools defined with name, description, parameters (JSON Schema format)
- Agent uses schemas to understand when and how to call tools
- Tool execution is separate from definition (execution in Spec-2)

**Decision**: Define tool schemas using MCP SDK format; agent suggests calls but doesn't execute

**Rationale**:
- Required by Phase-III constraints
- Separates tool definition from execution (clean architecture)
- Enables tool reuse across different agents
- Provides validation framework for tool parameters

**Implementation Approach**:
```python
# Tool schema example
add_task_tool = {
    "name": "add_task",
    "description": "Create a new task for the user",
    "parameters": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Task title"},
            "description": {"type": "string", "description": "Task description"},
            "due_date": {"type": "string", "format": "date-time", "description": "Optional due date"}
        },
        "required": ["title"]
    }
}
```

**Tool Schemas Needed**:
1. `add_task` - Create new task
2. `list_tasks` - List user's tasks (with optional filters)
3. `update_task` - Update existing task
4. `complete_task` - Mark task as completed
5. `delete_task` - Delete task

### 3. Conversation Context Reconstruction

**Question**: How to efficiently rebuild conversation context from database on each request?

**Research Findings**:
- Conversation context = ordered list of messages (user, assistant, system)
- Agent requires messages in chronological order with role labels
- Context window limits: GPT-4 supports ~8K tokens (MVP: limit to 100 messages)
- Database query optimization: index on conversation_id and created_at

**Decision**: Load full conversation history from DB, format for agent, include in request

**Rationale**:
- Stateless architecture requirement (no in-memory cache)
- Enables conversation resumption after restart
- Provides full context for agent decision-making
- Simple implementation for MVP (optimization later if needed)

**Implementation Approach**:
```python
def rebuild_context(conversation_id: str, db: Session) -> List[Dict]:
    messages = db.query(Message)\
        .filter(Message.conversation_id == conversation_id)\
        .order_by(Message.created_at.asc())\
        .limit(100)\
        .all()

    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]
```

**Performance Considerations**:
- Index on (conversation_id, created_at) for fast retrieval
- Limit to 100 messages for MVP (pagination in future)
- Consider caching for high-traffic scenarios (future optimization)

**Alternatives Considered**:
- In-memory session cache: Rejected (violates stateless principle)
- Conversation summarization: Deferred (adds complexity, not needed for MVP)
- Partial context loading: Deferred (100 messages sufficient for MVP)

### 4. ChatKit UI Library Investigation

**Question**: Is ChatKit an existing library or should we build custom components?

**Research Findings**:
- ChatKit is not a standard React/Next.js library in npm registry
- Likely refers to custom chat UI components or a specific internal library
- Standard chat UI patterns: message list, input field, send button, typing indicators

**Decision**: Build custom chat UI components following standard patterns

**Rationale**:
- No existing ChatKit library found in public registries
- Custom components provide full control and customization
- Simple implementation using React components and Tailwind CSS (already in project)
- Can be built quickly for MVP

**Implementation Approach**:
- `ChatInterface.tsx` - Main container component
- `MessageList.tsx` - Display conversation history with auto-scroll
- `MessageInput.tsx` - Text input with send button
- Use existing Tailwind CSS for styling
- Integrate with chat API client

**Component Structure**:
```tsx
<ChatInterface>
  <MessageList messages={messages} />
  <MessageInput onSend={handleSend} />
</ChatInterface>
```

**Alternatives Considered**:
- Third-party chat libraries (react-chat-elements, stream-chat-react): Overkill for MVP
- Headless UI components: Adds dependency, not needed for simple chat

### 5. Agent Confirmation Pattern

**Question**: How should the agent handle confirmation for destructive actions?

**Research Findings**:
- Destructive actions: delete_task, complete_task (marks as done)
- Confirmation pattern: Agent suggests action, waits for user approval
- Two-step flow: 1) Agent proposes tool call, 2) User confirms or cancels

**Decision**: Agent returns tool call suggestion with confirmation prompt; user must explicitly approve

**Rationale**:
- User safety (prevents accidental deletions)
- Transparency (user sees what will happen before it happens)
- Aligns with FR-009 requirement
- Simple to implement (agent includes confirmation text in response)

**Implementation Approach**:
```python
# Agent response for destructive action
{
    "response": "I can delete task #5 'Buy groceries'. Would you like me to proceed?",
    "tool_calls": [
        {
            "tool": "delete_task",
            "parameters": {"task_id": 5},
            "requires_confirmation": true
        }
    ]
}

# User must respond with explicit confirmation
# "Yes, delete it" or "No, cancel"
```

**Confirmation Flow**:
1. User: "Delete task 5"
2. Agent: "I can delete task #5 'Buy groceries'. Would you like me to proceed?"
3. User: "Yes"
4. Agent: Executes tool call (in Spec-2)

## Technology Stack Decisions

### Backend Dependencies (additions to requirements.txt)

```
openai>=1.0.0              # OpenAI Agents SDK
mcp-sdk>=0.1.0             # Official MCP SDK for tool definitions
```

### Frontend Dependencies (additions to package.json)

```json
{
  "dependencies": {
    // No new dependencies needed - use existing React, Axios, Tailwind
  }
}
```

### Database Schema Extensions

**New Tables**:
1. `conversations` - Store conversation sessions
2. `messages` - Store individual messages

**Indexes**:
- `conversations(user_id)` - Fast lookup of user's conversations
- `messages(conversation_id, created_at)` - Fast chronological message retrieval

## Best Practices

### 1. Stateless Architecture
- No in-memory session state
- Rebuild context from DB on every request
- Agent receives full conversation history as input

### 2. Security
- JWT authentication on chat endpoint (existing pattern)
- Validate conversation ownership (user can only access their conversations)
- Sanitize user input before passing to agent
- Rate limiting on chat endpoint (30 requests/minute)

### 3. Error Handling
- Graceful degradation if agent API fails
- User-friendly error messages (no technical details exposed)
- Retry logic for transient failures
- Logging for debugging and audit

### 4. Performance
- Database query optimization (indexes on conversation_id, created_at)
- Limit conversation history to 100 messages (MVP)
- Consider async processing for long-running agent calls
- Monitor response times (target: <3 seconds)

### 5. Testing
- Unit tests for services (conversation, message, agent)
- Integration tests for chat endpoint
- Mock agent responses for predictable testing
- Test conversation context reconstruction logic

## Open Questions & Risks

### Open Questions
1. ✅ ChatKit library availability - RESOLVED: Build custom components
2. ⚠️ OpenAI API rate limits - RISK: May need request queuing for high traffic
3. ⚠️ Conversation history size limits - RISK: 100 messages may be insufficient for power users

### Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| OpenAI API downtime | High | Low | Implement retry logic, show user-friendly error |
| Agent response latency >3s | Medium | Medium | Optimize context size, consider async processing |
| Conversation history grows too large | Medium | Low | Implement pagination (future), limit to 100 messages (MVP) |
| Tool call parsing errors | Medium | Low | Validate tool schemas, comprehensive error handling |
| User confusion with confirmation flow | Low | Medium | Clear confirmation prompts, examples in UI |

## Next Steps

1. ✅ Research complete - all questions answered
2. → Proceed to Phase 1: Generate data-model.md
3. → Proceed to Phase 1: Generate contracts/chat-api.yaml
4. → Proceed to Phase 1: Generate quickstart.md
5. → Update agent context with new technologies
