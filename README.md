# E-Commerce Chatbot with RAG & Ollama

This is a modular Retrieval-Augmented Generation (RAG) based e-commerce chatbot using Ollama. The chatbot answers FAQs, recommends products, answers product-specific questions, summarizes customer reviews, and intelligently routes user queries using an LLM-based intent detector.

## System Architecture

1. **User Query** -> Intent Detection (Ollama)
2. **Routing** -> Routes to one of 4 modules: FAQ, Recommendation, Product QA, Review
3. **Retrieval** -> Embeddings (Sentence-Transformers) / TF-IDF / Pandas Matching
4. **Generation** -> Ollama (qwen2.5) generates natural language response.

## Modules

- **FAQ Module**: Semantic search using `sentence-transformers` (`all-MiniLM-L6-v2`).
- **Recommendation Module**: TF-IDF vectors for product descriptions to find top 3 matches, and Ollama to justify the recommendation.
- **Product Module**: TF-IDF matching to find the most relevant product, then RAG (Ollama) to answer specific questions using the product details as context.
- **Review Module**: Keyword extraction to find reviews, and Ollama for sentiment analysis and summarization.
- **Intent Module**: LLM-based query routing using Ollama to choose between FAQ, RECOMMENDATION, PRODUCT, and REVIEW.

## Project Structure

```text
ECommerceGPT/
├── chatbot.py
├── faq_module.py
├── recommendation_module.py
├── product_module.py
├── review_module.py
├── intent_module.py
├── data/
│   ├── faq.csv
│   ├── products.csv
│   └── reviews.csv
├── models/
│   └── faq_embeddings.npy
├── requirements.txt
└── README.md
```

## Setup & Execution

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Ollama:**
   Ensure Ollama is installed and running locally. Pull the required model:
   ```bash
   ollama pull qwen2.5
   ollama serve
   ```

3. **Run the Chatbot:**
   ```bash
   python chatbot.py
   ```

## Example Interaction

```text
You: Where is my parcel?
↓
Detected Intent: FAQ
↓
Assistant: Use the Track Order page with your order ID.

You: Recommend a gaming laptop
↓
Detected Intent: RECOMMENDATION
↓
Assistant: Among the retrieved products, I recommend Lenovo Laptop 3...
```
