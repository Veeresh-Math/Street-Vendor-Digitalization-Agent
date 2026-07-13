"""
Tests for the knowledge base module.
"""

import pytest
from backend.knowledge_base import get_all_documents, get_text_for_embedding, get_all_chunks


def test_get_all_documents():
    """Test knowledge base returns documents."""
    docs = get_all_documents()
    assert len(docs) >= 20
    assert all("id" in d for d in docs)
    assert all("title" in d for d in docs)
    assert all("content" in d for d in docs)
    assert all("category" in d for d in docs)
    assert all("tags" in d for d in docs)


def test_document_categories():
    """Test documents cover expected categories."""
    docs = get_all_documents()
    categories = set(d["category"] for d in docs)
    assert "Government Scheme" in categories
    assert "UPI Setup" in categories
    assert "Online Listing" in categories
    assert "City Data" in categories


def test_get_text_for_embedding():
    """Test embedding text generation."""
    doc = {
        "title": "Test Title",
        "content": "Test content here.",
        "tags": ["tag1", "tag2"],
    }
    text = get_text_for_embedding(doc)
    assert "Test Title" in text
    assert "Test content here." in text
    assert "tag1" in text
    assert "tag2" in text


def test_get_all_chunks():
    """Test chunks generation for embedding."""
    chunks = get_all_chunks()
    assert len(chunks) >= 20
    assert all(isinstance(c, tuple) for c in chunks)
    assert all(len(c) == 2 for c in chunks)
    # Each chunk is (text, metadata_dict)
    for text, meta in chunks:
        assert isinstance(text, str)
        assert isinstance(meta, dict)
        assert "id" in meta
        assert "title" in meta


def test_documents_have_unique_ids():
    """Test all document IDs are unique."""
    docs = get_all_documents()
    ids = [d["id"] for d in docs]
    assert len(ids) == len(set(ids))
