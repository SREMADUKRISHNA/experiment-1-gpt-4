import pandas as pd
import numpy as np
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ProductModule:
    def __init__(self, data_path="data/products.csv"):
        self.df = pd.read_csv(data_path)
        self.tfidf = TfidfVectorizer()
        self.product_matrix = self.tfidf.fit_transform(self.df["ProductName"] + " " + self.df["Description"])

    def ask_ollama(self, prompt, model="qwen2.5:0.5b"):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False}
            )
            return response.json().get("response", "Error generating response.")
        except requests.exceptions.RequestException:
            return "Error: Could not connect to local Ollama instance."

    def answer_question(self, query):
        q_vec = self.tfidf.transform([query])
        scores = cosine_similarity(q_vec, self.product_matrix)[0]
        
        best_idx = np.argmax(scores)
        best_score = scores[best_idx]
        best_product = self.df.iloc[best_idx]
        
        prompt = (
            f"You are a helpful e-commerce assistant.\n"
            f"A customer asks: '{query}'\n\n"
            f"Here are the details for the most relevant product:\n"
            f"Product Name: {best_product['ProductName']}\n"
            f"Brand: {best_product['Brand']}\n"
            f"Category: {best_product['Category']}\n"
            f"Price: ₹{best_product['Price']}\n"
            f"Description: {best_product['Description']}\n"
            f"Rating: {best_product['Rating']}\n\n"
            f"Answer the customer's question clearly in 2-3 sentences based ONLY on the provided context."
        )
        
        answer = self.ask_ollama(prompt)
        return best_product['ProductName'], best_score, answer
