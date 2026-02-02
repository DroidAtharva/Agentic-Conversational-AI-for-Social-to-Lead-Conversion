from typing import List, Dict, Any

class AgentState:
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.intent: str = ""
        self.user_info: Dict[str, str] = {}
        self.lead_completed: bool = False
        self.lead_step: str = ""
        self.lead_captured: bool = False
        self.collecting_lead: bool = False

    def update_intent(self, intent: str):
        self.intent = intent

    def add_message(self, role: str, content: str):
        self.conversation_history.append({"role": role, "content": content})

    def get_last_user_message(self) -> str:
        for msg in reversed(self.conversation_history):
            if msg["role"] == "user":
                return msg["content"]
        return ""

    def is_lead_complete(self) -> bool:
        return all(key in self.user_info for key in ["name", "email", "platform"])

    def collect_lead_info(self, key: str, value: str):
        self.user_info[key] = value

    def start_lead_collection(self):
        self.lead_step = "name"
        self.lead_captured = False
        self.collecting_lead = True

    def next_lead_step(self):
        if self.lead_step == "name":
            self.lead_step = "email"
        elif self.lead_step == "email":
            self.lead_step = "platform"
        elif self.lead_step == "platform":
            self.lead_step = ""
            self.lead_captured = True
            self.collecting_lead = False

    def get_current_question(self) -> str:
        if self.lead_step == "name":
            return "What's your name?"
        elif self.lead_step == "email":
            return "What's your email address?"
        elif self.lead_step == "platform":
            return "What's your creator platform (e.g., YouTube, Instagram)?"
        return ""
