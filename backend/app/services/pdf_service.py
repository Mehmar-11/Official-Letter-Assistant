import base64
from io import BytesIO

import fitz  # pymupdf
import pdfplumber
from PIL import Image, ImageOps, UnidentifiedImageError

from app.config import MAX_PDF_PAGES
from app.services.llm_service import extract_text_from_image_with_llm


MIN_EXTRACTED_TEXT_LENGTH = 50
MAX_OCR_IMAGE_EDGE = 2400
MAX_OCR_IMAGE_PIXELS = 40_000_000


def prepare_image_for_ocr(image_bytes: bytes) -> bytes:
    """Normalize phone images before sending them to the vision model."""
    try:
        with Image.open(BytesIO(image_bytes)) as source:
            if source.width * source.height > MAX_OCR_IMAGE_PIXELS:
                raise ValueError("The image dimensions are too large.")

            image = ImageOps.exif_transpose(source)
            image.thumbnail(
                (MAX_OCR_IMAGE_EDGE, MAX_OCR_IMAGE_EDGE),
                Image.Resampling.LANCZOS,
            )

            if image.mode in ("RGBA", "LA"):
                background = Image.new("RGB", image.size, "white")
                alpha = image.getchannel("A")
                background.paste(image, mask=alpha)
                image = background
            elif image.mode != "RGB":
                image = image.convert("RGB")

            output = BytesIO()
            image.save(output, format="JPEG", quality=90, optimize=True)
            return output.getvalue()
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("Could not read the uploaded image.") from exc


def extract_text_from_image_bytes(image_bytes: bytes) -> str:
    """
    Extract text from an image file (JPEG/PNG) using GPT-4o Vision.
    """
    normalized_image = prepare_image_for_ocr(image_bytes)
    img_base64 = base64.b64encode(normalized_image).decode("utf-8")
    extracted_text = extract_text_from_image_with_llm(
        img_base64,
        media_type="image/jpeg",
    ).strip()

    if not extracted_text:
        raise ValueError("Could not extract any text from this image.")

    return extracted_text


def extract_text_from_scanned_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from a scanned or image-based PDF using GPT-4o Vision.
    Each page is converted to an image and sent to the LLM.
    """
    all_text = []

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as exc:
        raise ValueError("Could not read the uploaded PDF file.") from exc

    with doc:
        if doc.page_count > MAX_PDF_PAGES:
            raise ValueError(
                f"PDF files may contain at most {MAX_PDF_PAGES} pages."
            )

        for page in doc:
            pix = page.get_pixmap(dpi=200)
            img_bytes = pix.tobytes("png")
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")
            page_text = extract_text_from_image_with_llm(
                img_base64,
                media_type="image/png",
            )
            if page_text.strip():
                all_text.append(page_text.strip())

    if not all_text:
        raise ValueError("Could not extract any text from this scanned PDF.")

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
            if len(pdf.pages) > MAX_PDF_PAGES:
                raise ValueError(
                    f"PDF files may contain at most {MAX_PDF_PAGES} pages."
                )

            for page in pdf.pages:
                page_text = page.extract_text() or ""
                if page_text.strip():
                    extracted_pages.append(page_text.strip())
    except ValueError:
        raise
    except Exception:
        pass

    extracted_text = "\n\n".join(extracted_pages).strip()

    if len(extracted_text) >= MIN_EXTRACTED_TEXT_LENGTH:
        return extracted_text

    return extract_text_from_scanned_pdf(pdf_bytes)
