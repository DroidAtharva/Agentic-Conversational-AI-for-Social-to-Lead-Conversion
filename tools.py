def mock_lead_capture(name: str, email: str, platform: str):
    print(f"Lead captured successfully: {name}, {email}, {platform}")

class LeadCaptureTool:
    def __init__(self):
        self.required_fields = ["name", "email", "platform"]
        self.field_questions = {
            "name": "What's your name?",
            "email": "What's your email address?",
            "platform": "What's your creator platform (e.g., YouTube, Instagram)?"
        }

    def get_next_question(self, collected_info: dict) -> str:
        for field in self.required_fields:
            if field not in collected_info:
                return self.field_questions[field]
        return ""

    def capture_lead(self, collected_info: dict):
        if all(field in collected_info for field in self.required_fields):
            mock_lead_capture(
                collected_info["name"],
                collected_info["email"],
                collected_info["platform"]
            )
            return True
        return False
