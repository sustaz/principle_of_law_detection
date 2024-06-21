from docx import Document

def write_text_to_docx(text, file_path):
    """
    Write the given text to a .docx file.

    :param text: The text to write to the file.
    :param file_path: The path to the .docx file.
    """
    # Create a new Document
    doc = Document()

    # Add text to the document
    doc.add_paragraph(text)

    # Save the document to the specified file path
    doc.save(file_path)