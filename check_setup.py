"""
Quick start script to verify installation and setup.

Run this after installing dependencies to check everything works.
"""

import sys


def check_imports():
    """Check if all required packages are installed."""
    print("🔍 Checking required packages...")
    
    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("google.generativeai", "Google Generative AI"),
        ("sentence_transformers", "Sentence Transformers"),
        ("numpy", "NumPy"),
        ("dotenv", "python-dotenv"),
    ]
    
    missing = []
    for package, name in packages:
        try:
            __import__(package)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - MISSING")
            missing.append(name)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All packages installed!")
    return True


def check_env():
    """Check if .env file exists and has required variables."""
    print("\n🔍 Checking environment configuration...")
    
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            print("  ❌ GEMINI_API_KEY not configured")
            print("     1. Copy .env.example to .env")
            print("     2. Add your Gemini API key")
            print("     3. Get key from: https://makersuite.google.com/app/apikey")
            return False
        
        print("  ✅ GEMINI_API_KEY configured")
        print(f"     Key starts with: {api_key[:8]}...")
        return True
        
    except FileNotFoundError:
        print("  ❌ .env file not found")
        print("     Copy .env.example to .env")
        return False


def check_structure():
    """Check if directory structure is correct."""
    print("\n🔍 Checking project structure...")
    
    import os
    
    required_paths = [
        "app/main.py",
        "app/config.py",
        "app/api/routes.py",
        "app/agent/agent.py",
        "app/agent/prompts.py",
        "app/models/schemas.py",
        "app/services/llm.py",
        "app/services/embeddings.py",
        "app/templates/index.html",
    ]
    
    missing = []
    for path in required_paths:
        if os.path.exists(path):
            print(f"  ✅ {path}")
        else:
            print(f"  ❌ {path} - MISSING")
            missing.append(path)
    
    if missing:
        print(f"\n❌ Missing files: {len(missing)}")
        return False
    
    print("\n✅ Project structure correct!")
    return True


def main():
    """Run all checks."""
    print("=" * 60)
    print("🚀 AI Agent Demo - Installation Verification")
    print("=" * 60)
    print()
    
    checks = [
        check_imports(),
        check_env(),
        check_structure(),
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ ALL CHECKS PASSED!")
        print("\nYou're ready to run the application:")
        print("  python -m app.main")
        print("\nOr:")
        print("  uvicorn app.main:app --reload")
        print("\nThen open: http://localhost:8000")
    else:
        print("❌ SOME CHECKS FAILED")
        print("\nPlease fix the issues above before running the application.")
    print("=" * 60)
    
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
