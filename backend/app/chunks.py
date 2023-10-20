def generate_chunks(text, max_chunk_size=2000):
    chunks = []
    current_chunk = ""

    for char in text:
        if len(current_chunk) + 1 <= max_chunk_size:
            current_chunk += char
        else:
            chunks.append(current_chunk)
            current_chunk = char

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


if __name__ == "__main__":
    # Example usage:
    text = "Your long text here..."
    chunks = generate_chunks(text, max_chunk_size=5)
    for i, chunk in enumerate(chunks, start=1):
        print(f"Chunk {i}:\n{chunk}")
