import os

from langchain_text_splitters import RecursiveCharacterTextSplitter




KNOWLEDGE_BASE_DIR = "knowledge_base"




def load_documents():
    """
    Read every .txt file from the knowledge_base folder.

    Returns:
        A list of dictionaries containing:
        - filename
        - content
    """

    documents = []



    if not os.path.exists(KNOWLEDGE_BASE_DIR):

        print(
            f" Knowledge base folder not found: "
            f"{KNOWLEDGE_BASE_DIR}"
        )

        return documents

 

    for filename in os.listdir(KNOWLEDGE_BASE_DIR):

        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(
            KNOWLEDGE_BASE_DIR,
            filename
        )

        try:

       

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

         

            documents.append(
                {
                    "filename": filename,
                    "content": content
                }
            )

            print(
                f" Loaded: {filename}"
            )

        except Exception as e:

            print(
                f" Error reading {filename}: {e}"
            )


    return documents




def split_documents(documents):
    """
    Split large medical guideline documents
    into smaller chunks.

    Each chunk keeps information about
    its original source file.

    Returns:
        A list of dictionaries containing:
        - text
        - source
    """



    text_splitter = RecursiveCharacterTextSplitter(

   
        chunk_size=500,

       
        chunk_overlap=50
    )

    chunks = []



    for document in documents:

        filename = document["filename"]
        content = document["content"]

       
        split_texts = text_splitter.split_text(
            content
        )



        for text in split_texts:

            chunks.append(
                {
                    "text": text,
                    "source": filename
                }
            )

    print(
        f"\n Created {len(chunks)} chunks "
        f"from {len(documents)} documents."
    )

    return chunks




if __name__ == "__main__":

    print(
        "\n========== Loading Knowledge Base ==========\n"
    )



    documents = load_documents()

    print(
        f"\n Total documents loaded: "
        f"{len(documents)}"
    )

 

    for document in documents:

        print("\n" + "=" * 60)

        print(
            f"FILE: {document['filename']}"
        )

        print("=" * 60)

        print(
            document["content"]
        )



    print(
        "\n========== Splitting Documents ==========\n"
    )

    chunks = split_documents(documents)



    for i, chunk in enumerate(chunks, start=1):

        print("\n" + "=" * 60)

        print(
            f"CHUNK {i}"
        )

        print(
            f"SOURCE: {chunk['source']}"
        )

        print("=" * 60)

        print(
            chunk["text"]
        )

    print(
        "\n========== Loading and Splitting Completed ==========\n"
    )