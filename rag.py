import json
import os
from typing import List, Dict, Any

class KnowledgeBase:
    def __init__(self, file_path: str = "data/knowledge_base.json"):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self) -> Dict[str, Any]:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        return {}

    def search(self, query: str) -> str:
        query_lower = query.lower()
        response_parts = []

        # Handle pricing queries
        if "pricing" in query_lower or "price" in query_lower or "cost" in query_lower or "plan" in query_lower:
            pricing = self.data.get("pricing", {})
            response_parts.append("Here are our pricing plans:")
            for plan, details in pricing.items():
                plan_name = plan.title()
                price = details.get("price", "N/A")
                response_parts.append(f"\n{plan_name} Plan – {price}")
                videos = details.get("videos", "")
                if videos:
                    response_parts.append(f"• {videos}")
                resolution = details.get("resolution", "")
                if resolution:
                    response_parts.append(f"• {resolution} resolution")
                features = details.get("features", "")
                if features:
                    response_parts.append(f"• {features}")
            return "\n".join(response_parts)

        # Handle feature queries
        if "feature" in query_lower:
            pricing = self.data.get("pricing", {})
            response_parts.append("Here are our features:")
            for plan, details in pricing.items():
                plan_name = plan.title()
                features = details.get("features", "")
                if features:
                    response_parts.append(f"{plan_name} Plan: {features}")
            if response_parts:
                return "\n".join(response_parts)

        # Handle policy queries
        if "refund" in query_lower or "support" in query_lower or "policy" in query_lower:
            policies = self.data.get("policies", {})
            for policy, desc in policies.items():
                response_parts.append(f"{policy.title()}: {desc}")
            if response_parts:
                return "\n".join(response_parts)

        return "I'm sorry, I don't have information on that topic."
