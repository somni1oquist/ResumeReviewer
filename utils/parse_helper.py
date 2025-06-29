def parse_resume(file) -> str:
    """
    Parse a resume file and return its content as Markdown text.

    Args:
        file: A file-like object containing the resume data.
    Returns:
        str: The content of the resume in Markdown format.
    Raises:
        ValueError: If the file type is unsupported or if text extraction fails.
    """
    import mimetypes
    mime_type, _ = mimetypes.guess_type(file.name)
    file.seek(0)
    if mime_type == "application/pdf":
        return _parse_pdf(file)
    elif mime_type in ("application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                       "application/msword"):
        return _parse_docx(file)
    elif mime_type == "text/plain":
        return _parse_txt(file)
    else:
        raise ValueError("Unsupported file type")

def _parse_pdf(file) -> str:
    """
    Parse PDF files and return their content as Markdown text.
    """
    import pymupdf4llm, pymupdf
    file.seek(0)
    file_bytes = file.read()
    with pymupdf.open(stream=file_bytes, filetype="pdf") as doc:
        md_text = pymupdf4llm.to_markdown(doc)
        if not md_text.strip():
            raise ValueError("Failed to extract text from PDF")
        return md_text

def _parse_docx(file) -> str:
    """
    Parse DOCX files and return their content as text.
    """
    import docx2txt
    return docx2txt.process(file)

def _parse_txt(file) -> str:
    """
    Parse plain text files and return their content as a string.
    """
    return file.read().decode("utf-8")

