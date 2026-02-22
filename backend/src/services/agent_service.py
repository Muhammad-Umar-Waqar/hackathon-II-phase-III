from typing import List, Dict, Any, Optional
import os
import json
from ..utils.logger import logger, log_agent_invocation, log_agent_response, log_agent_error


class AgentService:
    """Service for AI agent integration supporting multiple providers (Gemini, OpenAI, OpenRouter)"""

    def __init__(self):
        self.provider = os.getenv("CHAT_PROVIDER", "gemini").lower()

        # Initialize clients based on available API keys
        self.gemini_client = None
        self.openai_client = None

        # Try to initialize Gemini
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=gemini_key)

                print("Available models:")
                for model in self.gemini_client.models.list():  # iterate directly
                    print("-", model.name)
# GEMINI_API_KEY=AIzaSyAtee1ZLlyvaILuTOE7EcRIoZAA1SqLllE

                self.gemini_model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
                logger.info(f"Gemini client initialized successfully with model: {self.gemini_model_name} and {gemini_key}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                raise Exception(f"Gemini initialization failed: {e}")

        # Initialize OpenAI
        if self.provider == "openai":
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key and openai_key != "sk-your-openai-api-key-here" and openai_key.startswith("sk-"):
                try:
                    from openai import OpenAI
                    self.openai_client = OpenAI(api_key=openai_key)
                    self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
                    self.openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
                    logger.info("OpenAI client initialized successfully")
                except Exception as e:
                    logger.error(f"Failed to initialize OpenAI: {e}")
                    raise Exception(f"OpenAI initialization failed: {e}")

        # Initialize OpenRouter (OpenAI-compatible API)
        if self.provider == "openrouter":
            openrouter_key = os.getenv("OPEN_ROUTER_API_KEY")
            if openrouter_key and openrouter_key.startswith("sk-or-"):
                try:
                    from openai import OpenAI
                    self.openai_client = OpenAI(
                        api_key=openrouter_key,
                        base_url="https://openrouter.ai/api/v1"
                    )
                    self.openai_model = os.getenv("OPEN_ROUTER_MODEL", "arcee-ai/trinity-large-preview:free")
                    self.openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
                    logger.info(f"OpenRouter client initialized successfully with model: {self.openai_model}")
                except Exception as e:
                    logger.error(f"Failed to initialize OpenRouter: {e}")
                    raise Exception(f"OpenRouter initialization failed: {e}")
            else:
                raise Exception("OpenRouter API key not found or invalid. Check OPEN_ROUTER_API_KEY in .env")

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

        # Define tools in both formats
        self._init_tool_schemas()

    def _init_tool_schemas(self):
        """Initialize tool schemas for both OpenAI and Gemini formats"""

        # OpenAI format (JSON schema)
        self.openai_tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "Optional description of the task"},
                            "due_date": {"type": "string", "description": "Optional due date in ISO format (YYYY-MM-DD)"}
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
                            "status": {"type": "string", "enum": ["pending", "in-progress", "completed"], "description": "Filter tasks by status"}
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
                            "task_id": {"type": "integer", "description": "The ID of the task to update"},
                            "title": {"type": "string", "description": "New title for the task"},
                            "description": {"type": "string", "description": "New description for the task"},
                            "status": {"type": "string", "enum": ["pending", "in-progress", "completed"], "description": "New status for the task"},
                            "due_date": {"type": "string", "description": "New due date in ISO format (YYYY-MM-DD)"}
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
                            "task_id": {"type": "integer", "description": "The ID of the task to complete"}
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
                            "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

        # Gemini format will be built dynamically in _get_gemini_tools()

    def _get_gemini_tools(self):
        """Build Gemini function declarations for new google-genai SDK"""
        from google.genai import types

        return [
            types.Tool(
                function_declarations=[
                    types.FunctionDeclaration(
                        name="add_task",
                        description="Create a new task for the user",
                        parameters={
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
                    ),
                    types.FunctionDeclaration(
                        name="list_tasks",
                        description="List all tasks for the user, optionally filtered by status",
                        parameters={
                            "type": "object",
                            "properties": {
                                "status": {
                                    "type": "string",
                                    "description": "Filter tasks by status (pending, in-progress, completed)"
                                }
                            }
                        }
                    ),
                    types.FunctionDeclaration(
                        name="update_task",
                        description="Update an existing task",
                        parameters={
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
                                    "description": "New status for the task (pending, in-progress, completed)"
                                },
                                "due_date": {
                                    "type": "string",
                                    "description": "New due date in ISO format (YYYY-MM-DD)"
                                }
                            },
                            "required": ["task_id"]
                        }
                    ),
                    types.FunctionDeclaration(
                        name="complete_task",
                        description="Mark a task as completed. Requires user confirmation.",
                        parameters={
                            "type": "object",
                            "properties": {
                                "task_id": {
                                    "type": "integer",
                                    "description": "The ID of the task to complete"
                                }
                            },
                            "required": ["task_id"]
                        }
                    ),
                    types.FunctionDeclaration(
                        name="delete_task",
                        description="Delete a task permanently. Requires user confirmation.",
                        parameters={
                            "type": "object",
                            "properties": {
                                "task_id": {
                                    "type": "integer",
                                    "description": "The ID of the task to delete"
                                }
                            },
                            "required": ["task_id"]
                        }
                    )
                ]
            )
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
        Uses the provider specified in CHAT_PROVIDER env variable
        """
        try:
            # Log agent invocation
            if conversation_id and user_id:
                log_agent_invocation(conversation_id, user_id, user_message)

            # Use only the configured provider (no fallback)
            if self.provider == "gemini":
                if not self.gemini_client:
                    raise Exception("Gemini client not initialized. Check GEMINI_API_KEY in .env")
                return self._process_with_gemini(user_message, conversation_history, conversation_id, user_id)
            elif self.provider == "openai":
                if not self.openai_client:
                    raise Exception("OpenAI client not initialized. Check OPENAI_API_KEY in .env")
                return self._process_with_openai(user_message, conversation_history, conversation_id, user_id)
            elif self.provider == "openrouter":
                if not self.openai_client:
                    raise Exception("OpenRouter client not initialized. Check OPEN_ROUTER_API_KEY in .env")
                return self._process_with_openai(user_message, conversation_history, conversation_id, user_id)
            else:
                raise Exception(f"Invalid CHAT_PROVIDER: {self.provider}. Must be 'gemini', 'openai', or 'openrouter'")

        except Exception as e:
            if conversation_id and user_id:
                log_agent_error(conversation_id, user_id, e)
            logger.error(f"Error in AgentService.process_message: {str(e)}")
            raise

    def _process_with_gemini(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]],
        conversation_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Process message using Gemini with new google-genai SDK"""
        from google.genai import types

        # Build conversation context
        messages = [{"role": "user", "parts": [{"text": self.system_prompt}]}]

        # Add conversation history
        if conversation_history:
            for msg in conversation_history:
                role = "user" if msg["role"] == "user" else "model"
                messages.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })

        # Add current user message
        messages.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })

        # Generate content with tools
        response = self.gemini_client.models.generate_content(
            model=self.gemini_model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=self._get_gemini_tools(),
                temperature=0.7
            )
        )

        # Extract response text
        response_text = ""
        if response.text:
            response_text = response.text

        # Extract function calls
        tool_calls = []
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        fc = part.function_call
                        tool_name = fc.name
                        tool_params = dict(fc.args) if fc.args else {}

                        requires_confirmation = tool_name in ["delete_task", "complete_task"]

                        tool_calls.append({
                            "tool": tool_name,
                            "parameters": tool_params,
                            "requires_confirmation": requires_confirmation
                        })

        # Log response
        if conversation_id and user_id:
            log_agent_response(conversation_id, user_id, response_text, tool_calls)

        return {
            "response": response_text,
            "tool_calls": tool_calls
        }

    def _process_with_openai(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]],
        conversation_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Process message using OpenAI"""
        # Build messages
        messages = [{"role": "system", "content": self.system_prompt}]

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": user_message})

        # Call OpenAI API
        response = self.openai_client.chat.completions.create(
            model=self.openai_model,
            messages=messages,
            max_tokens=self.openai_max_tokens,
            temperature=0.7,
            tools=self.openai_tools,
            tool_choice="auto"
        )

        # Extract response
        assistant_message = response.choices[0].message
        response_text = assistant_message.content or ""

        # Extract tool calls
        tool_calls = []
        if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_params = json.loads(tool_call.function.arguments)

                requires_confirmation = tool_name in ["delete_task", "complete_task"]

                tool_calls.append({
                    "tool": tool_name,
                    "parameters": tool_params,
                    "requires_confirmation": requires_confirmation
                })

        # Log response
        if conversation_id and user_id:
            log_agent_response(conversation_id, user_id, response_text, tool_calls)

        return {
            "response": response_text,
            "tool_calls": tool_calls
        }

    def format_conversation_history(self, messages: List[Any]) -> List[Dict[str, str]]:
        """Format message objects into conversation history format"""
        history = []
        for msg in messages:
            history.append({
                "role": msg.role,
                "content": msg.content
            })
        return history
