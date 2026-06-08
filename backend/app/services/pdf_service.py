from io import BytesIO

import pdfplumber
import base64
import fitz  # pymupdf


MIN_EXTRACTED_TEXT_LENGTH = 50

def extract_text_from_scanned_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from a scanned or image-based PDF using GPT-4o Vision.
    Each page is converted to an image and sent to the LLM.
    """
    from app.services.llm_service import extract_text_from_image_with_llm

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    all_text = []

    for page in doc:
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        page_text = extract_text_from_image_with_llm(img_base64)
        if page_text.strip():
            all_text.append(page_text.strip())

    doc.close()

    if not all_text:
        raise ValueError(
            "Could not extract any text from this scanned PDF."
        )

    return "\n\n".join(all_text)

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text from a PDF file.
    Tries text-based extraction first. If that fails or returns too little text,
    falls back to OCR using GPT-4o Vision for scanned or image-based PDFs.
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
    except Exception:
        pass

    extracted_text = "\n\n".join(extracted_pages).strip()

    if len(extracted_text) >= MIN_EXTRACTED_TEXT_LENGTH:
        return extracted_text

    return extract_text_from_scanned_pdf(pdf_bytes)