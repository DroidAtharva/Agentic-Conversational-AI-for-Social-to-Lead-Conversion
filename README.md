# Agentic-Conversational-AI-for-Social-to-Lead-Conversion
🧠 Social-to-Lead Conversational AI Agent

This project implements a stateful, agentic Conversational AI system that converts user conversations into qualified business leads.
It goes beyond a traditional chatbot by combining intent detection, Retrieval-Augmented Generation (RAG), explicit state management, and guarded tool execution.

The agent is built for a fictional SaaS product AutoStream, which provides automated video editing tools for content creators.

✨ Key Capabilities

✅ Intent Identification

Classifies user intent into:

Casual greeting

Product / pricing inquiry

High-intent lead (ready to sign up)

📚 RAG-Powered Knowledge Retrieval

Answers pricing and policy questions using a local knowledge base

Prevents hallucination by grounding responses in factual data

🧠 Stateful Multi-Turn Conversations

Retains memory across multiple conversation turns

Tracks collected user details and conversation progress

🔐 Guarded Tool Execution

Captures leads only after all required information is collected

Prevents premature or unsafe backend actions

🖥️ Interactive UI

Streamlit-based chat interface for real-time interaction

🏗️ Project Architecture (High-Level)
User (Streamlit UI)
        ↓
Intent Detection
        ↓
Decision Logic (State)
        ↓
RAG Knowledge Retrieval
        ↓
Tool Execution (Lead Capture)


The entire system revolves around explicit state management, ensuring reliability and control across multi-turn conversations.

📁 Project Structure
.
├── agent/
│   ├── agent.py        # Agent orchestration & decision logic
│   ├── intent.py       # Intent classification
│   ├── rag.py          # RAG pipeline using local knowledge base
│   ├── state.py        # Conversation state management
│   └── tools.py        # Backend tool (lead capture)
│
├── data/
│   └── knowledge_base.json   # Pricing & policy data
│
├── streamlit_app.py    # Streamlit UI
├── main.py             # Entry point (CLI / local run)
├── test_agent.py       # Basic testing
├── requirements.txt
└── README.md

🔍 How It Works (Step-by-Step)

User Input

User sends a message via the Streamlit UI

Intent Detection

The system classifies the intent of the message

Determines whether the user is exploring or ready to convert

Decision Logic

Based on intent and conversation state, the agent decides:

Answer via RAG

Ask for lead details

Trigger backend action

RAG (Retrieval-Augmented Generation)

Relevant information is retrieved from knowledge_base.json

The LLM generates a grounded response using retrieved data

State Update

User-provided details (name, email, platform) are stored incrementally

Tool Execution

Once all required fields are collected, the lead capture tool is executed safely

🧠 Why RAG Is Used

RAG ensures:

Accurate pricing information

Consistent policy answers

Zero hallucination for business-critical data

All knowledge is stored locally and retrieved dynamically, making updates easy without code changes.

⚙️ Tech Stack

Language: Python 3.9+

UI: Streamlit

LLM: GPT-4o-mini / Gemini 1.5 Flash / Claude 3 Haiku

Architecture Pattern: Agentic workflow with explicit state management

Knowledge Base: JSON (local)

Backend Actions: Mock API tool for lead capture

▶️ How to Run Locally
1️⃣ Clone the repository
git clone <repo-url>
cd <repo-name>

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Set environment variables

Create a .env file:

OPENAI_API_KEY=your_api_key_here

4️⃣ Run the Streamlit app
streamlit run streamlit_app.py

📦 Lead Capture Tool
def mock_lead_capture(name, email, platform):
    print(f"Lead captured successfully: {name}, {email}, {platform}")


The tool is triggered only when all required fields are present, ensuring safe and deterministic execution.

📲 WhatsApp Integration (Conceptual)

To integrate this agent with WhatsApp:

Use WhatsApp Business API

Receive messages via Webhook

Forward messages to the agent backend

Maintain state per user using session IDs

Send agent responses back through WhatsApp API

This architecture supports real-time, scalable deployment.

🎯 Key Learnings

Agentic systems require control flow, not just prompts

State management is critical for real-world AI reliability

Tool execution must be logic-driven, not model-driven

RAG is essential for factual accuracy in production systems

📌 Conclusion

This project demonstrates how to build a production-style conversational AI agent that combines reasoning, memory, and action — moving beyond chatbots to real-world AI systems.
