from sentence_transformers import SentenceTransformer


print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

text = "Metformin and kidney function"

embedding = model.encode(text)

print("\nOriginal text:")
print(text)

print("\nEmbedding generated successfully.")

print("Embedding length:")
print(len(embedding))

print("\nFirst 10 values:")
print(embedding[:10])