# AutoStream Conversational AI Agent

This project implements a conversational AI agent for AutoStream, a SaaS product providing automated video editing tools for content creators. The agent classifies user intents, retrieves information from a local knowledge base, and captures leads when users show high intent.

## How to Run the Project Locally

1. Ensure Python 3.9+ is installed.
2. Install dependencies: `pip install -r requirements.txt`
3. (Optional) Set up OpenAI API key in a `.env` file: `OPENAI_API_KEY=your_key_here`
4. Run the agent: `python main.py`
5. Interact with the agent in the console. Type 'quit' to exit.

## Architecture Explanation

The AutoStream AI Agent is built using standard Python with a modular architecture for maintainability and simplicity. The core components include:

- **State Management (state.py)**: Maintains conversation history, detected intent, user information, and lead completion status across multiple turns using a simple class-based approach.

- **Intent Classification (intent.py)**: Uses keyword-based matching to classify user messages into three categories: greeting, product_or_pricing_inquiry, and high_intent_lead. This deterministic approach ensures consistent intent detection without relying on external models.

- **Knowledge Retrieval (rag.py)**: Implements a simplified RAG system by searching a local JSON knowledge base for relevant information. It matches query keywords to pricing, features, and policy data, returning accurate responses without hallucinations.

- **Lead Capture (tools.py)**: Manages the lead collection process, asking for name, email, and platform sequentially. The mock_lead_capture function is called only when all required information is collected.

- **Main Agent (main.py)**: Orchestrates the conversation flow, integrating all components. It uses OpenAI's API if available, falling back to a mock LLM for responses. The console-based interface allows for interactive testing.

This architecture prioritizes robustness and simplicity, avoiding complex frameworks while ensuring stateful, context-aware conversations. The agent can handle multi-turn dialogues, retrieve accurate information, and capture leads efficiently.

## WhatsApp Integration

To integrate this agent with WhatsApp, use the WhatsApp Business API with webhooks. Set up a Flask or FastAPI server to receive webhook messages from WhatsApp. When a message is received, extract the user input, process it through the agent, and send the response back via the WhatsApp API. Handle message threading by storing conversation state in a database (e.g., SQLite or Redis) keyed by user phone number. Ensure compliance with WhatsApp's rate limits and message formatting requirements. Use ngrok or a similar tool for local development to expose the webhook endpoint.
