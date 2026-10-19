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
    Load FAISS index and metadata.
    """

  
    if not os.path.exists(INDEX_PATH):

        raise FileNotFoundError(
            f" FAISS index not found: {INDEX_PATH}"
        )

    if not os.path.exists(METADATA_PATH):

        raise FileNotFoundError(
            f" Metadata file not found: {METADATA_PATH}"
        )

  
    index = faiss.read_index(
        INDEX_PATH
    )

    with open(
        METADATA_PATH,
        "rb"
    ) as file:

        metadata = pickle.load(file)

    print(
        " FAISS index loaded."
    )

    print(
        "Metadata loaded."
    )

    print(
        f" Number of vectors: {index.ntotal}"
    )

    print(
        f"Number of metadata records: {len(metadata)}"
    )

    return index, metadata



def extract_chunk_text(metadata_record):
    """
    Extract actual text from a metadata record.

    Supports different possible metadata formats.
    """



    if isinstance(
        metadata_record,
        dict
    ):

        
        possible_keys = [
            "content",
            "text",
            "chunk",
            "page_content"
        ]

        for key in possible_keys:

            value = metadata_record.get(
                key
            )

            if value is not None:

                value = str(value).strip()

                if value:

                    return value

      
        for key, value in metadata_record.items():

            if isinstance(
                value,
                str
            ):

                value = value.strip()

                if value:

                    if key.lower() not in [
                        "filename",
                        "source",
                        "file"
                    ]:

                        return value

        return ""

   
    if isinstance(
        metadata_record,
        str
    ):

        return metadata_record.strip()

 
    return ""



def extract_filename(metadata_record):
    """
    Extract filename from metadata.
    """

    if isinstance(
        metadata_record,
        dict
    ):

        for key in [
            "filename",
            "source",
            "file"
        ]:

            value = metadata_record.get(
                key
            )

            if value:

                return str(value)

    return "Unknown"


def retrieve_relevant_chunks(
    query,
    top_k=3
):
    """
    Search the medical knowledge base
    using semantic similarity.
    """

    print(
        "\n========== Knowledge Retrieval ==========\n"
    )


    if not query:

        print(
            " Query is empty."
        )

        return []

    if not isinstance(
        query,
        str
    ):

        print(
            " Query must be a string."
        )

        return []

    query = query.strip()

    if not query:

        print(
            " Query is empty."
        )

        return []

    print(
        f"Search Query:\n{query}"
    )

 
    try:

        index, metadata = load_vector_store()

    except Exception as e:

        print(
            f" Could not load vector store: {e}"
        )

        return []

    try:

        print(
            "\nCreating query embedding..."
        )

        query_embedding = create_embedding(
            query
        )

        print(
            " Query embedding created."
        )

    except Exception as e:

        print(
            f" Could not create query embedding: {e}"
        )

        return []


    try:

       

        if isinstance(
            query_embedding,
            list
        ) and len(query_embedding) > 0:

            first_item = query_embedding[0]

            if isinstance(
                first_item,
                dict
            ):

                # Try common embedding keys
                possible_keys = [
                    "embedding",
                    "vector",
                    "values"
                ]

                found_vector = None

                for key in possible_keys:

                    if key in first_item:

                        found_vector = first_item[key]

                        break

                if found_vector is not None:

                    query_embedding = found_vector

     

        query_vector = np.asarray(
            query_embedding,
            dtype="float32"
        )

  

        if query_vector.ndim > 1:

            query_vector = query_vector.reshape(
                -1
            )



        query_vector = query_vector.reshape(
            1,
            -1
        )

        print(
            f" Query vector shape: {query_vector.shape}"
        )

    except Exception as e:

        print(
            f"❌ Could not convert query embedding: {e}"
        )

        return []

   

    if query_vector.shape[1] != index.d:

        print(
            "\n❌ EMBEDDING DIMENSION MISMATCH"
        )

        print(
            f"Query dimension : {query_vector.shape[1]}"
        )

        print(
            f"FAISS dimension : {index.d}"
        )

        print(
            "\nThe same embedding model must be used "
            "for both the vector store and the query."
        )

        return []


    search_k = min(
        top_k,
        index.ntotal
    )

    try:

        distances, indices = index.search(
            query_vector,
            search_k
        )

    except Exception as e:

        print(
            f"❌ FAISS search failed: {e}"
        )

        return []



    results = []

    print(
        "\n========== RETRIEVED KNOWLEDGE =========="
    )

    for position in range(
        len(indices[0])
    ):

        index_id = int(
            indices[0][position]
        )


        if index_id < 0:

            continue

        if index_id >= len(metadata):

            print(
                f"⚠️ Invalid metadata index: {index_id}"
            )

            continue

      

        metadata_record = metadata[
            index_id
        ]

  

        print(
            f"\nMetadata index: {index_id}"
        )

        print(
            f"Metadata type: {type(metadata_record)}"
        )

        if isinstance(
            metadata_record,
            dict
        ):

            print(
                f"Metadata keys: "
                f"{list(metadata_record.keys())}"
            )



        chunk = extract_chunk_text(
            metadata_record
        )

        filename = extract_filename(
            metadata_record
        )

    

        if not chunk:

            print(
                f"⚠️ No text found for metadata index "
                f"{index_id}"
            )

            continue

   

        distance = float(
            distances[0][position]
        )

        

        result = {

            "rank": len(results) + 1,

            "index_id": index_id,

            "distance": distance,

            "filename": filename,

            "content": chunk
        }

        results.append(
            result
        )


        print(
            f"\nResult {result['rank']}"
        )

        print(
            f"Source: {filename}"
        )

        print(
            f"Distance: {distance}"
        )

        print(
            f"Content:\n{chunk}"
        )

   

    print(
        "\n=========================================="
    )

    if results:

        print(
            f" Retrieved {len(results)} "
            f"relevant chunk(s)."
        )

    else:

        print(
            " No relevant knowledge chunks found."
        )

        print(
            "\nThis usually means the metadata does not "
            "contain the chunk text."
        )

    return results




def search_knowledge_base(
    query,
    top_k=3
):
    """
    Public function used by the Medical Agent
    to search the medical knowledge base.
    """

    return retrieve_relevant_chunks(
        query=query,
        top_k=top_k
    )




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


    print(
        "\n========== SEARCH RESULTS ==========\n"
    )

    if not results:

        print(
            " No relevant knowledge found."
        )

    else:

        for i, result in enumerate(
            results,
            start=1
        ):

            print(
                f"\n----- Result {i} -----"
            )

            print(
                f"Rank: {result['rank']}"
            )

            print(
                f"Source: {result['filename']}"
            )

            print(
                f"Distance: {result['distance']}"
            )

            print(
                f"Content:\n{result['content']}"
            )

            print(
                "-" * 60
            )

    print(
        "\n========== Retrieval Completed ==========\n"
    )