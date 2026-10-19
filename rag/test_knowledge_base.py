import os


KNOWLEDGE_BASE_DIR = "knowledge_base"


def load_knowledge_base():
    documents = []

    for filename in os.listdir(KNOWLEDGE_BASE_DIR):

        if filename.endswith(".txt"):

            filepath = os.path.join(
                KNOWLEDGE_BASE_DIR,
                filename
            )

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            documents.append({
                "filename": filename,
                "content": content
            })

    return documents


if __name__ == "__main__":

    documents = load_knowledge_base()

    print(
        f"\nFound {len(documents)} knowledge-base documents.\n"
    )

    for document in documents:

        print("=" * 60)

        print(
            f"FILE: {document['filename']}"
        )

        print("=" * 60)

        print(
            document["content"][:500]
        )

        print()