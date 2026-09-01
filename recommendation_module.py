import pandas as pd
import numpy as np
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationModule:
    def __init__(self, data_path="data/products.csv"):
        self.df = pd.read_csv(data_path)
        self.tfidf = TfidfVectorizer()
        self.product_matrix = self.tfidf.fit_transform(self.df["Description"])

    def ask_ollama(self, prompt, model="qwen2.5:0.5b"):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False}
            )
            return response.json().get("response", "Error generating response.")
        except requests.exceptions.RequestException:
            return "Error: Could not connect to local Ollama instance."

    def recommend(self, query):
        q_vec = self.tfidf.transform([query])
        scores = cosine_similarity(q_vec, self.product_matrix)[0]
        
        # Get top 3 indices
        top3_idx = np.argsort(scores)[::-1][:3]
        top3_products = self.df.iloc[top3_idx]
        
        results_str = top3_products[["ProductName", "Brand", "Price"]].to_string(index=False)
        
        # Use Ollama for justification
        prompt = (
            f"User is looking for: '{query}'.\n"
            f"Top 3 matches from our database:\n{results_str}\n"
            f"Please recommend the best option among these 3 and provide a brief, professional justification."
        )
        reasoning = self.ask_ollama(prompt)
        
        return top3_products, reasoning
