from .ingestion import load_documents


def chunk_text(text, chunk_size=500):

    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # If adding this paragraph stays within the limit
        if len(current_chunk) + len(paragraph) <= chunk_size:

            if current_chunk:
                current_chunk += "\n\n"

            current_chunk += paragraph

        else:

            # Save the current chunk
            if current_chunk:
                chunks.append(current_chunk)

            # Start a new chunk
            current_chunk = paragraph

    # Add the final chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


if __name__ == "__main__":

    documents = load_documents()

    for document in documents:

        chunks = chunk_text(document["text"])

        print(f"\nSource: {document['source']}")
        print(f"Number of chunks: {len(chunks)}")

        for i, chunk in enumerate(chunks):

            print(f"\nChunk {i + 1}:")
            print(chunk)
            print("-" * 60)