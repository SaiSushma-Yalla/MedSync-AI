import os
import pickle
import faiss
import numpy as np

from rag.embeddings import create_embedding



VECTOR_STORE_DIR = "vector_store"

INDEX_PATH = os.path.join(
    VECTOR_STORE_DIR,
    "medical_guidelines.index"
)

METADATA_PATH = os.path.join(
    VECTOR_STORE_DIR,
    "medical_guidelines.pkl"
)




def load_vector_store():
    """
    Load the FAISS index and metadata from disk.
    """

    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError(
            f"❌ FAISS index not found: {INDEX_PATH}"
        )

    if not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(
            f"❌ Metadata file not found: {METADATA_PATH}"
        )

   
    index = faiss.read_index(
        INDEX_PATH
    )


    with open(
        METADATA_PATH,
        "rb"
    ) as file:

        metadata = pickle.load(file)

    print(" FAISS index loaded.")
    print(" Metadata loaded.")
    print(
        f" Number of vectors: {index.ntotal}"
    )
    print(
        f" Number of metadata records: {len(metadata)}"
    )

    return index, metadata




def search_knowledge_base(
    query,
    top_k=3
):
    """
    Search the medical knowledge base
    using semantic similarity.

    Parameters:
        query: User/agent question
        top_k: Number of relevant chunks to retrieve

    Returns:
        List of relevant knowledge chunks.
    """

    print(
        "\n========== KNOWLEDGE BASE SEARCH ==========\n"
    )

  

    if not query or not isinstance(query, str):

        print(
            " Query must be a non-empty string."
        )

        return []


    try:

        index, metadata = load_vector_store()

    except Exception as e:

        print(
            f" Could not load vector store: {e}"
        )

        return []



    try:

        query_embedding = create_embedding(
            query
        )

    except Exception as e:

        print(
            f" Could not create query embedding: {e}"
        )

        return []

    

    query_vector = np.array(
        [query_embedding],
        dtype="float32"
    )



    try:

        distances, indices = index.search(
            query_vector,
            top_k
        )

    except Exception as e:

        print(
            f"FAISS search failed: {e}"
        )

        return []

 

    results = []

   

    for position, index_id in enumerate(
        indices[0]
    ):

      
        if index_id == -1:
            continue

    
        if index_id >= len(metadata):
            continue


        metadata_record = metadata[index_id]

        

        if isinstance(
            metadata_record,
            dict
        ):

            content = metadata_record.get(
                "content",
                ""
            )

            filename = metadata_record.get(
                "filename",
                "Unknown"
            )

        else:

            content = str(
                metadata_record
            )

            filename = "Unknown"

        

        if not content.strip():
            continue


        distance = float(
            distances[0][position]
        )

        

        result = {

            "rank": len(results) + 1,

            "score": distance,

            "filename": filename,

            "content": content
        }

        results.append(
            result
        )


    if len(results) == 0:

        print(
            " No relevant knowledge found."
        )

    else:

        print(
            f" Retrieved {len(results)} relevant chunk(s)."
        )

        for result in results:

            print(
                f"\n----- Result {result['rank']} -----"
            )

            print(
                f"Source: {result['filename']}"
            )

            print(
                f"Score: {result['score']}"
            )

            print(
                f"Content:\n{result['content']}"
            )

    print(
        "\n=========================================="
    )

    return results




if __name__ == "__main__":

    query = (
        "Metformin chronic kidney disease "
        "dosage recommendations"
    )

    print(
        "\n========== KNOWLEDGE BASE SEARCH ==========\n"
    )

    results = search_knowledge_base(
        query,
        top_k=3
    )

    for i, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n----- Result {i} -----"
        )

        print(
            f"Source: {result['filename']}"
        )

        print(
            f"Score: {result['score']}"
        )

        print(
            f"Content:\n{result['content']}"
        )