from faq_module import FAQModule
from recommendation_module import RecommendationModule
from product_module import ProductModule
from review_module import ReviewModule
from intent_module import IntentModule
import warnings

# Ignore warning messages for clean output
warnings.filterwarnings('ignore')

class ECommerceChatbot:
    def __init__(self):
        print("Initializing Chatbot modules... Please wait.")
        self.intent_module = IntentModule()
        self.faq_module = FAQModule()
        self.recommendation_module = RecommendationModule()
        self.product_module = ProductModule()
        self.review_module = ReviewModule()
        print("Initialization complete!\n")

    def run(self):
        print("=== E-Commerce Chatbot (type 'exit' or 'quit' to close) ===")
        
        while True:
            query = input("\nYou: ").strip()
            if query.lower() in ['exit', 'quit']:
                print("Bot: Goodbye! Have a great day.")
                break
                
            if not query:
                continue

            intent = self.intent_module.detect_intent(query)
            print(f"---\nDetected Intent: {intent}\n---")

            if intent == "FAQ":
                q, a, score = self.faq_module.search(query)
                if score > 0.4:
                    print(f"Assistant: {a}")
                else:
                    # Use Ollama as fallback if confidence is low
                    prompt = f"Answer this general e-commerce question concisely: {query}"
                    fallback_answer = self.faq_module.embed_model # Hack to reuse imports, just doing normal request
                    import requests
                    try:
                        res = requests.post("http://localhost:11434/api/generate", json={"model": "qwen2.5:0.5b", "prompt": prompt, "stream": False}).json()["response"]
                        print(f"Assistant: {res}")
                    except:
                        print("Assistant: I'm sorry, I couldn't understand that and my backend is offline.")

            elif intent == "RECOMMENDATION":
                print("Assistant:")
                top_products, reasoning = self.recommendation_module.recommend(query)
                print(reasoning)

            elif intent == "PRODUCT":
                prod_name, score, answer = self.product_module.answer_question(query)
                print(f"Assistant:\n{answer}")

            elif intent == "REVIEW":
                # Basic extraction of potential product name
                words = query.split()
                # A very naive extraction - in reality we might want another LLM call or NER
                prod_guess = query.replace("reviews", "").replace("review", "").replace("what do people think about", "").replace("tell me about", "").strip(' ?.')
                print("Assistant:")
                print(self.review_module.summarize_reviews(prod_guess))

if __name__ == "__main__":
    bot = ECommerceChatbot()
    bot.run()
