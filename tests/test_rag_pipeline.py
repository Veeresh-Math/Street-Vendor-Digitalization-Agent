"""
Tests for the RAG pipeline module (non-IBM parts).
Tests the prompt builder, cache integration, and index management logic.
"""

import pytest
from unittest.mock import patch, MagicMock
from backend.rag_pipeline import _build_prompt, is_index_ready, index_doc_count


class TestBuildPrompt:
    """Tests for the _build_prompt function."""

    def test_basic_prompt_structure(self):
        retrieved = [
            {
                "id": "test_01",
                "title": "Test Document",
                "category": "Government Scheme",
                "text": "Test content about PM SVANidhi.",
                "distance": 0.2,
                "score": 0.8,
            }
        ]
        prompt = _build_prompt("How to get a loan?", retrieved, language="en")
        assert "Street Vendor Agent" in prompt
        assert "Government Scheme" in prompt
        assert "How to get a loan?" in prompt
        assert "Reply in simple English." in prompt

    def test_hindi_language_instruction(self):
        retrieved = [
            {
                "id": "test_01",
                "title": "UPI Setup",
                "category": "UPI Setup",
                "text": "Steps to set up UPI.",
                "distance": 0.1,
                "score": 0.9,
            }
        ]
        prompt = _build_prompt("UPI kaise setup karein?", retrieved, language="hi")
        assert "Hindi" in prompt

    def test_tamil_language_instruction(self):
        retrieved = [
            {
                "id": "test_01",
                "title": "UPI Setup",
                "category": "UPI Setup",
                "text": "Steps to set up UPI.",
                "distance": 0.1,
                "score": 0.9,
            }
        ]
        prompt = _build_prompt("UPI setup", retrieved, language="ta")
        assert "Tamil" in prompt

    def test_multiple_retrieved_docs(self):
        retrieved = [
            {
                "id": "test_01",
                "title": "Doc One",
                "category": "Category A",
                "text": "Content one.",
                "distance": 0.1,
                "score": 0.9,
            },
            {
                "id": "test_02",
                "title": "Doc Two",
                "category": "Category B",
                "text": "Content two.",
                "distance": 0.2,
                "score": 0.8,
            },
        ]
        prompt = _build_prompt("test query", retrieved, language="en")
        assert "[1]" in prompt
        assert "[2]" in prompt
        assert "Category A" in prompt
        assert "Category B" in prompt

    def test_unknown_language_defaults_to_english(self):
        retrieved = [
            {
                "id": "test_01",
                "title": "Test",
                "category": "Test",
                "text": "Test.",
                "distance": 0.1,
                "score": 0.9,
            }
        ]
        prompt = _build_prompt("test", retrieved, language="xx")
        assert "Reply in simple English." in prompt

    def test_prompt_contains_context(self):
        retrieved = [
            {
                "id": "test_01",
                "title": "Test",
                "category": "Test",
                "text": "Test content.",
                "distance": 0.1,
                "score": 0.9,
            }
        ]
        prompt = _build_prompt("test", retrieved, language="en")
        assert "Context:" in prompt
        assert "Answer briefly" in prompt
