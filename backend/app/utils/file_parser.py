"""
File parsing utilities for different document formats.

Supports: .txt, .md, .pdf
"""

import io
from pypdf import PdfReader


class FileParser:
    """
    Parse different file formats and extract text content.
    """
    
    @staticmethod
    def parse_text(content: bytes, filename: str) -> str:
        """
        Parse file content based on file extension.
        
        Args:
            content: Raw file bytes
            filename: Original filename with extension
            
        Returns:
            Extracted text content
            
        Raises:
            ValueError: If file format is unsupported
            UnicodeDecodeError: If text file is not UTF-8
            Exception: If PDF parsing fails
        """
        file_ext = filename.lower().split('.')[-1]
        
        if file_ext in ['txt', 'md', 'markdown']:
            return FileParser._parse_text_file(content)
        elif file_ext == 'pdf':
            return FileParser._parse_pdf(content)
        else:
            raise ValueError(
                f"Unsupported file format: .{file_ext}. "
                "Supported formats: .txt, .md, .pdf"
            )
    
    @staticmethod
    def _parse_text_file(content: bytes) -> str:
        """
        Parse plain text or markdown file.
        
        Args:
            content: Raw file bytes
            
        Returns:
            Decoded text content
            
        Raises:
            UnicodeDecodeError: If file is not UTF-8 encoded
        """
        return content.decode('utf-8')
    
    @staticmethod
    def _parse_pdf(content: bytes) -> str:
        """
        Extract text from PDF file.
        
        Args:
            content: Raw PDF bytes
            
        Returns:
            Extracted text from all pages
            
        Raises:
            Exception: If PDF parsing fails
        """
        try:
            # Create PDF reader from bytes
            pdf_file = io.BytesIO(content)
            reader = PdfReader(pdf_file)
            
            # Extract text from all pages
            text_parts = []
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text.strip():
                    text_parts.append(page_text)
            
            if not text_parts:
                raise ValueError("PDF contains no extractable text")
            
            # Join all pages with double newline
            return "\n\n".join(text_parts)
        
        except Exception as e:
            raise Exception(f"Failed to parse PDF: {str(e)}")
    
    @staticmethod
    def get_supported_extensions() -> list[str]:
        """
        Get list of supported file extensions.
        
        Returns:
            List of supported extensions (without dots)
        """
        return ['txt', 'md', 'markdown', 'pdf']
    
    @staticmethod
    def is_supported(filename: str) -> bool:
        """
        Check if file format is supported.
        
        Args:
            filename: Filename with extension
            
        Returns:
            True if supported, False otherwise
        """
        file_ext = filename.lower().split('.')[-1]
        return file_ext in FileParser.get_supported_extensions()
