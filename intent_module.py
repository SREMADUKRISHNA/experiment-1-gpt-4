import requests

class IntentModule:
    def __init__(self, model="qwen2.5:0.5b"):
        self.model = model

    def ask_ollama(self, prompt):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False}
            )
            return response.json().get("response", "FAQ").strip()
        except requests.exceptions.RequestException:
            return "FAQ"

    def detect_intent(self, query):
        prompt = (
            f"Analyze the following user query and classify it into exactly ONE of the following intents:\n"
            f"1. FAQ (General questions about shipping, returns, payment, policies)\n"
            f"2. RECOMMENDATION (Asking for product suggestions, best options)\n"
            f"3. PRODUCT (Asking for specific details, price, or specs of a certain product)\n"
            f"4. REVIEW (Asking for opinions, ratings, sentiment, or reviews about a product)\n\n"
            f"User Query: '{query}'\n\n"
            f"Respond ONLY with the intent name (FAQ, RECOMMENDATION, PRODUCT, or REVIEW)."
        )
        
        intent = self.ask_ollama(prompt).upper()
        
        # Clean up in case the LLM returned extra text
        valid_intents = ["FAQ", "RECOMMENDATION", "PRODUCT", "REVIEW"]
        for valid in valid_intents:
            if valid in intent:
                return valid
                
        return "FAQ" # Default fallback
