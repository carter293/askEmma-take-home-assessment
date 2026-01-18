from fastapi import UploadFile, HTTPException

ALLOWED_EXTS = {"txt", "md"}
ALLOWED_CT = {"text/plain", "text/markdown", "text/x-markdown"}
MAX_BYTES = 1_000_000  # 1MB


def ext_of(name: str) -> str:
    """Extract file extension from filename."""
    if "." not in name:
        return ""
    return name.rsplit(".", 1)[1].lower()


async def process_uploaded_file(file: UploadFile) -> str:
    """
    Validate and extract text content from an uploaded file.

    Args:
        file: The uploaded file to process

    Returns:
        The decoded text content of the file

    Raises:
        HTTPException: If validation fails (invalid extension, content-type, size, or encoding)
    """
    # 1) Extension check
    ext = ext_of(file.filename or "")
    if ext not in ALLOWED_EXTS:
        raise HTTPException(status_code=400, detail="Only .txt or .md files allowed")

    # 2) Content-type check
    if file.content_type and file.content_type not in ALLOWED_CT:
        raise HTTPException(status_code=400, detail=f"Invalid content type: {file.content_type}")

    # 3) Size limit (streamed)
    size = 0
    chunks = []
    while True:
        chunk = await file.read(64 * 1024)
        if not chunk:
            break
        size += len(chunk)
        if size > MAX_BYTES:
            raise HTTPException(status_code=413, detail="File too large")
        chunks.append(chunk)

    data = b"".join(chunks)

    # 4) Ensure it's text (UTF-8 decode check)
    try:
        file_text = data.decode("utf-8").strip()
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 text")

    return file_text
