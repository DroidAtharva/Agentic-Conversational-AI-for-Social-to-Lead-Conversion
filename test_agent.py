from agent.agent import run_agent, AgentState

def test_agent():
    state = AgentState(
        messages=[],
        intent="",
        user_info={},
        lead_captured=False,
        current_question=""
    )

    # Test 1: Casual greeting
    print("Test 1: Casual greeting")
    state = run_agent("Hi there", state)
    print(f"Response: {state['messages'][-1]['content']}")
    print(f"Intent: {state['intent']}\n")

    # Reset state for next test
    state = AgentState(
        messages=[],
        intent="",
        user_info={},
        lead_captured=False,
        current_question=""
    )

    # Test 2: Pricing inquiry
    print("Test 2: Pricing inquiry")
    state = run_agent("Tell me about your pricing", state)
    print(f"Response: {state['messages'][-1]['content']}")
    print(f"Intent: {state['intent']}\n")

    # Reset state
    state = AgentState(
        messages=[],
        intent="",
        user_info={},
        lead_captured=False,
        current_question=""
    )

    # Test 3: High intent lead
    print("Test 3: High intent lead")
    state = run_agent("That sounds good, I want to try the Pro plan for my YouTube channel", state)
    print(f"Response: {state['messages'][-1]['content']}")
    print(f"Intent: {state['intent']}")
    # Simulate providing name
    state = run_agent("John Doe", state)
    print(f"Response: {state['messages'][-1]['content']}")
    # Simulate providing email
    state = run_agent("john@example.com", state)
    print(f"Response: {state['messages'][-1]['content']}")
    # Simulate providing platform
    state = run_agent("YouTube", state)
    print(f"Response: {state['messages'][-1]['content']}")
    print(f"Lead captured: {state['lead_captured']}")
    print(f"User info: {state['user_info']}\n")

if __name__ == "__main__":
    test_agent()
