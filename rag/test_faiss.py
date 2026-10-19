import faiss
import numpy as np



vectors = np.array(
    [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
        [0.7, 0.8, 0.9]
    ],
    dtype="float32"
)



index = faiss.IndexFlatL2(3)


index.add(vectors)

print("Number of vectors stored:")
print(index.ntotal)



query = np.array(
    [[0.1, 0.2, 0.3]],
    dtype="float32"
)

distances, indices = index.search(
    query,
    2
)

print("\nNearest vectors:")
print(indices)

print("\nDistances:")
print(distances)