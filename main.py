import os
import sys
from agent.state import AgentState
from agent.intent import IntentClassifier
from agent.rag import KnowledgeBase
from agent.tools import LeadCaptureTool

class MockLLM:
    def generate_response(self, prompt: str) -> str:
        # Simple mock responses based on keywords
        prompt_lower = prompt.lower()
        if "greeting" in prompt_lower:
            return "Hello! How can I help you with AutoStream today?"
        elif "pricing" in prompt_lower or "price" in prompt_lower:
            return "We have Basic and Pro plans. Basic is $29/month for 10 videos in 720p. Pro is $79/month for unlimited videos in 4K with AI captions."
        elif "lead" in prompt_lower:
            return "Great! Let's get you signed up."
        else:
            return "I'm here to help with AutoStream. What would you like to know?"

class AutoStreamAgent:
    def __init__(self):
        self.state = AgentState()
        self.intent_classifier = IntentClassifier()
        self.knowledge_base = KnowledgeBase()
        self.lead_tool = LeadCaptureTool()
        
        # Try to use OpenAI, fallback to mock
        try:
            import openai
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                openai.api_key = api_key
                self.llm = openai.OpenAI()
            else:
                self.llm = MockLLM()
        except ImportError:
            self.llm = MockLLM()

    def process_message(self, user_message: str) -> str:
        self.state.add_message("user", user_message)
        
        response = ""
        
        # LEAD COLLECTION MODE (LOCKED)
        if self.state.collecting_lead:
            # Accept the user's reply as the value for the current lead_step
            if self.state.lead_step == "name":
                self.state.collect_lead_info("name", user_message)
            elif self.state.lead_step == "email":
                self.state.collect_lead_info("email", user_message)
            elif self.state.lead_step == "platform":
                self.state.collect_lead_info("platform", user_message)
            
            self.state.next_lead_step()
            
            if self.state.lead_captured:
                if self.lead_tool.capture_lead(self.state.user_info):
                    response = "Thank you! Your lead has been captured successfully."
            else:
                response = self.state.get_current_question()
        
        # POST-LEAD BEHAVIOR
        elif self.state.lead_captured:
            # Classify intent to handle repeated high-intent
            intent = self.intent_classifier.classify(user_message)
            if intent == "high_intent_lead":
                response = "Lead already captured. Thank you for your interest!"
            else:
                response = "I'm here to help with AutoStream. What would you like to know?"
        
        # DEFAULT MODE
        else:
            # Run intent classification normally
            intent = self.intent_classifier.classify(user_message)
            self.state.update_intent(intent)
            
            if intent == "greeting":
                response = "Hello! How can I help you with AutoStream today?"
            
            elif intent == "product_or_pricing_inquiry":
                # Retrieve knowledge
                knowledge = self.knowledge_base.search(user_message)
                response = knowledge
            
            elif intent == "high_intent_lead":
                # HIGH-INTENT DETECTED
                self.state.start_lead_collection()
                response = self.state.get_current_question()
            
            else:
                response = "I'm here to help with AutoStream. What would you like to know?"
        
        self.state.add_message("assistant", response)
        return response

def main():
    agent = AutoStreamAgent()
    print("AutoStream AI Agent")
    print("Type 'quit' to exit")
    print("-" * 50)
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'quit':
            break
        
        response = agent.process_message(user_input)
        print(f"Agent: {response}")
        print()

if __name__ == "__main__":
    main()
