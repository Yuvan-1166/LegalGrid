#!/usr/bin/env python3
"""Quick test to verify setup is working"""

import sys
from app.core.config import settings

def test_imports():
    """Test that all required packages are installed"""
    print("Testing imports...")
    try:
        import fastapi
        import qdrant_client
        import sentence_transformers
        import groq
        import langchain
        print("✓ All packages imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    print(f"  Project: {settings.PROJECT_NAME}")
    print(f"  Version: {settings.VERSION}")
    print(f"  Environment: {settings.ENVIRONMENT}")
    print(f"  Qdrant URL: {settings.QDRANT_URL}")
    print(f"  GROQ API Key: {'✓ Set' if settings.GROQ_API_KEY else '✗ Not set'}")
    
    if not settings.GROQ_API_KEY:
        print("\n⚠️  Warning: GROQ_API_KEY not set in .env file")
        print("   Get your free API key from: https://console.groq.com")
        return False
    
    print("✓ Configuration loaded")
    return True

def test_qdrant_connection():
    """Test Qdrant connection"""
    print("\nTesting Qdrant connection...")
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(url=settings.QDRANT_URL)
        # Try to get collections (will fail if Qdrant not running)
        collections = client.get_collections()
        print(f"✓ Connected to Qdrant at {settings.QDRANT_URL}")
        print(f"  Collections: {len(collections.collections)}")
        return True
    except Exception as e:
        print(f"✗ Qdrant connection failed: {e}")
        print("\n  Make sure Qdrant is running:")
        print("  docker-compose up -d")
        return False

def test_embeddings():
    """Test embedding model"""
    print("\nTesting embedding model...")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-mpnet-base-v2")
        test_text = "This is a test sentence"
        embedding = model.encode(test_text)
        print(f"✓ Embedding model loaded")
        print(f"  Embedding dimension: {len(embedding)}")
        return True
    except Exception as e:
        print(f"✗ Embedding model failed: {e}")
        return False

def main():
    print("=" * 60)
    print("LegalGrid Backend Setup Test")
    print("=" * 60)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Qdrant Connection", test_qdrant_connection()))
    results.append(("Embeddings", test_embeddings()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:.<40} {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All tests passed! Setup is complete.")
        print("\nNext steps:")
        print("  1. Run: python scripts/seed_data.py")
        print("  2. Run: python main.py")
        print("  3. Open: http://localhost:8000/docs")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
