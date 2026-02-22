from typing import List, Dict, Any, Optional
import os
from openai import OpenAI
from ..utils.logger import logger, log_agent_invocation, log_agent_response, log_agent_error


class AgentService:
    """Service for AI agent integration using OpenAI"""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))

        # System prompt for the todo assistant
        self.system_prompt = """You are a helpful todo assistant. You help users manage their tasks through natural language.

You can suggest the following actions:
- add_task: Create a new task
- list_tasks: Show all tasks
- update_task: Modify an existing task
- complete_task: Mark a task as completed
- delete_task: Remove a task

When users ask to perform actions, interpret their intent and suggest the appropriate tool call.
Always ask for confirmation before suggesting destructive actions (delete, complete).
If the user's intent is unclear, ask clarifying questions.
Be friendly, concise, and helpful."""

        # Tool schemas using OpenAI function calling format
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional description of the task"
                            },
                            "due_date": {
                                "type": "string",
                                "description": "Optional due date in ISO format (YYYY-MM-DD)"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for the user, optionally filtered by status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in-progress", "completed"],
                                "description": "Filter tasks by status"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title for the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description for the task"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in-progress", "completed"],
                                "description": "New status for the task"
                            },
                            "due_date": {
                                "type": "string",
                                "description": "New due date in ISO format (YYYY-MM-DD)"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed. Requires user confirmation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to complete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task permanently. Requires user confirmation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

    def process_message(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        conversation_id: str = None,
        user_id: str = None
    ) -> Dict[str, Any]:
        """
        Process a user message and get agent response

        Args:
            user_message: The user's message
            conversation_history: Previous messages in the conversation
            conversation_id: ID of the conversation
            user_id: ID of the user

        Returns:
            Dict with 'response' (str) and 'tool_calls' (list)
        """
        try:
            # Log agent invocation
            if conversation_id and user_id:
                log_agent_invocation(conversation_id, user_id, user_message)

            # Build messages for OpenAI
            messages = [{"role": "system", "content": self.system_prompt}]

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add current user message
            messages.append({"role": "user", "content": user_message})

            # Call OpenAI API with tools
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=0.7,
                tools=self.tools,
                tool_choice="auto"  # Let the model decide when to use tools
            )

            # Extract response
            assistant_message = response.choices[0].message
            response_text = assistant_message.content or ""

            # Extract tool calls if any (OpenAI function calling format)
            tool_calls = []
            if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
                for tool_call in assistant_message.tool_calls:
                    import json
                    tool_name = tool_call.function.name
                    tool_params = json.loads(tool_call.function.arguments)

                    # Check if this is a destructive action requiring confirmation
                    requires_confirmation = tool_name in ["delete_task", "complete_task"]

                    tool_calls.append({
                        "tool": tool_name,
                        "parameters": tool_params,
                        "requires_confirmation": requires_confirmation
                    })

                    # If confirmation required and not in response, add confirmation prompt
                    if requires_confirmation and response_text:
                        if "confirm" not in response_text.lower():
                            response_text += f"\n\nPlease confirm: Do you want to {tool_name.replace('_', ' ')}?"

            # Log agent response
            if conversation_id and user_id:
                log_agent_response(conversation_id, user_id, response_text, tool_calls)

            return {
                "response": response_text,
                "tool_calls": tool_calls
            }

        except Exception as e:
            if conversation_id and user_id:
                log_agent_error(conversation_id, user_id, e)
            logger.error(f"Error in AgentService.process_message: {str(e)}")
            raise

    def format_conversation_history(self, messages: List[Any]) -> List[Dict[str, str]]:
        """
        Format message objects into OpenAI conversation history format

        Args:
            messages: List of Message objects from database

        Returns:
            List of dicts with 'role' and 'content' keys
        """
        history = []
        for msg in messages:
            history.append({
                "role": msg.role,
                "content": msg.content
            })
        return history
