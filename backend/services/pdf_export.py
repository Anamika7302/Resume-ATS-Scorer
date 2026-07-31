
import logging
from typing import Dict

logger = logging.getLogger("ats_resume_scorer")


def generate_combined_pdf(html_docs: Dict[str, str]) -> bytes:
   
    try:
        from weasyprint import HTML
    except ImportError as e:
        logger.error("WeasyPrint is not installed.")
        raise ImportError(
            "WeasyPrint is required for PDF generation. "
            "Install it using: pip install weasyprint"
        ) from e

    if not html_docs:
        raise ValueError("No HTML documents provided.")

    # Render each HTML string into a WeasyPrint document
    documents = [HTML(string=html).render() for html in html_docs.values()]

    # Use the first document as the base
    merged_document = documents[0]

    # Append pages from the remaining documents
    for document in documents[1:]:
        merged_document.pages.extend(document.pages)

    # Return PDF bytes
    pdf_bytes = merged_document.write_pdf()

    if pdf_bytes is None:
        raise RuntimeError("PDF generation failed.")

    return pdf_bytes
