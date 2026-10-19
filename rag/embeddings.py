from langchain_huggingface import HuggingFaceEmbeddings




MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


print("\n========== Creating Embedding Model ==========\n")

try:

    embedding_model = HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )

    print(" Embedding model loaded successfully.")

except Exception as e:

    print(f" Failed to load embedding model: {e}")

    embedding_model = None




def create_embedding(text):
    """
    Convert text into a numerical embedding vector.

    Input:
        text -> string

    Output:
        list of floating-point numbers
    """

    if embedding_model is None:

        raise RuntimeError(
            "Embedding model is not loaded."
        )

    if not text or not isinstance(text, str):

        raise ValueError(
            "Text must be a non-empty string."
        )

    try:

        embedding = embedding_model.embed_query(
            text
        )

        return embedding

    except Exception as e:

        print(
            f" Error creating embedding: {e}"
        )

        raise




if __name__ == "__main__":

    print(
        "\n========== Testing Embedding ==========\n"
    )

    text = (
        "Metformin dosage should be considered "
        "when kidney function is reduced."
    )

    embedding = create_embedding(text)

    print(
        "\nEmbedding type:"
    )

    print(
        type(embedding)
    )

    print(
        "\nEmbedding dimension:"
    )

    print(
        len(embedding)
    )

    print(
        "\nFirst 10 values:"
    )

    print(
        embedding[:10]
    )

    print(
        "\n========== Embedding Test Completed ==========\n"
    )
    