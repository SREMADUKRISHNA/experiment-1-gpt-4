import pandas as pd
import requests

class ReviewModule:
    def __init__(self, data_path="data/reviews.csv"):
        self.df = pd.read_csv(data_path)

    def ask_ollama(self, prompt, model="qwen2.5:0.5b"):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False}
            )
            return response.json().get("response", "Error generating response.")
        except requests.exceptions.RequestException:
            return "Error: Could not connect to local Ollama instance."

    def summarize_reviews(self, product_name):
        # Case insensitive match
        rows = self.df[self.df["ProductName"].str.contains(product_name, case=False, na=False)]
        
        if rows.empty:
            return f"No reviews found for '{product_name}'."
            
        reviews_text = " | ".join(rows["Review"].tolist())
        
        prompt = (
            f"Here are some customer reviews for the product '{product_name}':\n"
            f"{reviews_text}\n\n"
            f"Please analyze these reviews and provide:\n"
            f"1. Overall Sentiment (Positive, Negative, or Neutral)\n"
            f"2. Key Strengths (bullet points)\n"
            f"3. Key Weaknesses (bullet points)\n"
            f"4. A final buying suggestion."
        )
        
        return self.ask_ollama(prompt)
