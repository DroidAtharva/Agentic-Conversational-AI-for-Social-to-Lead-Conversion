import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langgraph import StateGraph, END
from typing import TypedDict, List
import dotenv

dotenv.load_dotenv()

# Mock lead capture function
def mock_lead_capture(name, email, platform):
    print(f"Lead captured successfully: {name}, {email}, {platform}")

# Load knowledge base
with open('../data/knowledge_base.json', 'r') as f:
    knowledge_data = json.load(f)

# Prepare documents for RAG
documents = []
for category, items in knowledge_data.items():
    if isinstance(items, dict):
        for sub_category, details in items.items():
            if isinstance(details, dict):
                text = f"{sub_category}: " + ", ".join([f"{k}: {v}" for k, v in details.items()])
            else:
                text = f"{category}: {details}"
            documents.append(text)
    else:
        documents.append(f"{category}: {items}")

# Create vector store
embeddings = OpenAIEmbeddings()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.create_documents(documents)
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# State definition
class AgentState(TypedDict):
    messages: List[dict]
    intent: str
    user_info: dict
    lead_captured: bool
    current_question: str

# Intent classification
def classify_intent(state: AgentState):
    conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in state['messages']])
    prompt = f"Based on the conversation:\n{conversation}\nClassify the latest user intent: 1. Casual greeting, 2. Product or pricing inquiry, 3. High-intent lead (ready to sign up). Respond with only the number."
    response = llm([HumanMessage(content=prompt)]).content.strip()
    intent_map = {"1": "casual_greeting", "2": "inquiry", "3": "high_intent"}
    state['intent'] = intent_map.get(response, "inquiry")
    return state

# RAG retrieval
def retrieve_knowledge(state: AgentState):
    if state['intent'] == "inquiry":
        query = state['messages'][-1]['content']
        qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
        response = qa_chain.run(query)
        state['messages'].append({"role": "assistant", "content": response})
    elif state['intent'] == "casual_greeting":
        state['messages'].append({"role": "assistant", "content": "Hello! How can I help you with AutoStream today?"})
    return state

# Lead collection
def collect_lead_info(state: AgentState):
    if state['intent'] == "high_intent" and not state['lead_captured']:
        user_info = state['user_info']
        if 'name' not in user_info:
            state['current_question'] = "name"
            state['messages'].append({"role": "assistant", "content": "Great! To get you started, what's your name?"})
        elif 'email' not in user_info:
            state['current_question'] = "email"
            state['messages'].append({"role": "assistant", "content": "What's your email address?"})
        elif 'platform' not in user_info:
            state['current_question'] = "platform"
            state['messages'].append({"role": "assistant", "content": "What's your creator platform (e.g., YouTube, Instagram)?"})
        else:
            mock_lead_capture(user_info['name'], user_info['email'], user_info['platform'])
            state['lead_captured'] = True
            state['messages'].append({"role": "assistant", "content": "Thank you! Your lead has been captured successfully."})
    return state

# Define the graph
workflow = StateGraph(AgentState)

workflow.add_node("classify_intent", classify_intent)
workflow.add_node("retrieve_knowledge", retrieve_knowledge)
workflow.add_node("collect_lead", collect_lead_info)

workflow.set_entry_point("classify_intent")

workflow.add_edge("classify_intent", "retrieve_knowledge")
workflow.add_edge("retrieve_knowledge", "collect_lead")
workflow.add_edge("collect_lead", END)

app = workflow.compile()

# Function to run the agent
def run_agent(user_input: str, state: AgentState):
    state['messages'].append({"role": "user", "content": user_input})
    if state['intent'] == "high_intent" and not state['lead_captured']:
        if state['current_question'] == "name":
            state['user_info']['name'] = user_input
        elif state['current_question'] == "email":
            state['user_info']['email'] = user_input
        elif state['current_question'] == "platform":
            state['user_info']['platform'] = user_input
    result = app.invoke(state)
    return result
