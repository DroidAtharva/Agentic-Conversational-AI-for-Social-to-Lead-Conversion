class IntentClassifier:
    def __init__(self):
        self.intents = {
            "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
            "product_or_pricing_inquiry": ["pricing", "price", "cost", "plan", "feature", "what", "how much", "subscription"],
            "high_intent_lead": ["sign up", "register", "join", "interested", "start", "get started", "buy", "purchase", "try", "want to", "interested in"]
        }

    def classify(self, message: str) -> str:
        message_lower = message.lower()
        
        # Check for high_intent_lead first (more specific)
        for keyword in self.intents["high_intent_lead"]:
            if keyword in message_lower:
                return "high_intent_lead"
        
        # Check for product_or_pricing_inquiry
        for keyword in self.intents["product_or_pricing_inquiry"]:
            if keyword in message_lower:
                return "product_or_pricing_inquiry"
        
        # Default to greeting
        return "greeting"
