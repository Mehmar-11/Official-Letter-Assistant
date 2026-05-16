from io import BytesIO

import pdfplumber


MIN_EXTRACTED_TEXT_LENGTH = 50


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text from a text-based PDF.

    This function supports text-based PDFs for the MVP.
    Scanned or image-based PDFs require OCR and are treated as unsupported
    for now.
    """
    if not pdf_bytes:
        raise ValueError("The uploaded PDF file is empty.")

    extracted_pages = []

    try:
        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                if page_text.strip():
                    extracted_pages.append(page_text.strip())
    except Exception as exc:
        raise ValueError(
            "Could not read this PDF file. Please try another text-based PDF "
            "or paste the letter text manually."
        ) from exc

    extracted_text = "\n\n".join(extracted_pages).strip()

    if len(extracted_text) < MIN_EXTRACTED_TEXT_LENGTH:
        raise ValueError(
            "Could not extract readable text from this PDF. The file may be "
            "scanned, image-based, or contain too little selectable text. "
            "Please paste the letter text manually or try a text-based PDF."
        )

    return extracted_text