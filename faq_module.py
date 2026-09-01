import pandas as pd
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class FAQModule:
    def __init__(self, data_path="data/faq.csv", model_name="all-MiniLM-L6-v2"):
        self.df = pd.read_csv(data_path)
        self.embed_model = SentenceTransformer(model_name)
        self.embeddings = None
        self._load_or_create_embeddings()

    def _load_or_create_embeddings(self):
        embeddings_path = "models/faq_embeddings.npy"
        if os.path.exists(embeddings_path):
            self.embeddings = np.load(embeddings_path)
        else:
            print("Generating FAQ embeddings...")
            self.embeddings = self.embed_model.encode(self.df["Question"].tolist())
            np.save(embeddings_path, self.embeddings)

    def search(self, query, threshold=0.4):
        q_embed = self.embed_model.encode([query])
        scores = cosine_similarity(q_embed, self.embeddings)[0]
        best_idx = np.argmax(scores)
        best_score = scores[best_idx]
        
        if best_score > threshold:
            return self.df.iloc[best_idx]["Question"], self.df.iloc[best_idx]["Answer"], best_score
        return None, None, best_score
