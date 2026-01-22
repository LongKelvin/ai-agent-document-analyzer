"""
Test script for PDF parsing functionality.

Run this to verify PDF text extraction works correctly.
"""

from app.utils.file_parser import FileParser


def test_supported_formats():
    """Test file format detection."""
    print("\n" + "="*70)
    print("📋 SUPPORTED FORMAT TESTS")
    print("="*70 + "\n")
    
    test_cases = [
        ("document.txt", True),
        ("readme.md", True),
        ("notes.markdown", True),
        ("report.pdf", True),
        ("image.png", False),
        ("data.docx", False),
        ("sheet.xlsx", False),
    ]
    
    for filename, expected in test_cases:
        result = FileParser.is_supported(filename)
        status = "✓" if result == expected else "✗"
        print(f"{status} {filename:20} -> {'Supported' if result else 'Not supported'}")
    
    print("\n" + "="*70)
    print(f"✅ Supported extensions: {', '.join('.' + ext for ext in FileParser.get_supported_extensions())}")
    print("="*70 + "\n")


def test_text_parsing():
    """Test text file parsing."""
    print("\n" + "="*70)
    print("📄 TEXT FILE PARSING TEST")
    print("="*70 + "\n")
    
    # Test UTF-8 text
    test_content = "Hello, World! This is a test document.\nWith multiple lines.\n".encode('utf-8')
    
    try:
        text = FileParser.parse_text(test_content, "test.txt")
        print(f"✓ Successfully parsed text file")
        print(f"  Content length: {len(text)} characters")
        print(f"  Preview: {text[:50]}...")
    except Exception as e:
        print(f"✗ Failed to parse text file: {str(e)}")
    
    print()


def test_pdf_parsing():
    """Test PDF parsing (if a sample PDF is available)."""
    print("\n" + "="*70)
    print("📕 PDF PARSING TEST")
    print("="*70 + "\n")
    
    print("ℹ️  To test PDF parsing:")
    print("   1. Place a sample PDF file in the project root")
    print("   2. Update this test with the file path")
    print("   3. Run this script again")
    print()
    print("Example usage:")
    print("   with open('sample.pdf', 'rb') as f:")
    print("       content = f.read()")
    print("       text = FileParser.parse_text(content, 'sample.pdf')")
    print("       print(f'Extracted {len(text)} characters')")
    print()


def main():
    print("\n" + "="*70)
    print("🧪 FILE PARSER FUNCTIONALITY TESTS")
    print("="*70)
    
    test_supported_formats()
    test_text_parsing()
    test_pdf_parsing()
    
    print("\n" + "="*70)
    print("✅ ALL BASIC TESTS COMPLETED")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
