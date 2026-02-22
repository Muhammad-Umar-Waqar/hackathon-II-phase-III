import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from src.services.agent_service import AgentService

def test_chatbot():
    """Test the Gemini chatbot directly"""
    print("=" * 60)
    print("Testing Gemini Chatbot")
    print("=" * 60)
    
    try:
        # Initialize agent service
        print("\n1. Initializing Agent Service...")
        agent = AgentService()
        print(f"   [OK] Provider: {agent.provider}")
        print(f"   [OK] Gemini Client: {'Initialized' if agent.gemini_client else 'Not initialized'}")
        
        # Test 1: Simple greeting
        print("\n2. Test 1: Simple Greeting")
        print("   User: Hello!")
        response = agent.process_message("Hello!", conversation_history=None)
        print(f"   Assistant: {response['response']}")
        print(f"   Tool Calls: {response.get('tool_calls', [])}")
        
        # Test 2: List tasks request
        print("\n3. Test 2: List Tasks Request")
        print("   User: Show me all my tasks")
        response = agent.process_message("Show me all my tasks", conversation_history=None)
        print(f"   Assistant: {response['response']}")
        print(f"   Tool Calls: {response.get('tool_calls', [])}")
        
        # Test 3: Add task request
        print("\n4. Test 3: Add Task Request")
        print("   User: Add a task to buy groceries tomorrow")
        response = agent.process_message("Add a task to buy groceries tomorrow", conversation_history=None)
        print(f"   Assistant: {response['response']}")
        print(f"   Tool Calls: {response.get('tool_calls', [])}")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chatbot()
