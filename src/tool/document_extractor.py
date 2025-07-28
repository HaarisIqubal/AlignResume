from docling.document_converter import DocumentConverter

def extract_pdf_document(pdf_path: str):
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    markdown_content = result.document.export_to_markdown()
    return markdown_content