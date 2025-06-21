"""
Unit tests for Bible fetcher functionality.
Tests the BibleFetcher class and related functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

# Import the Bible fetcher module
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from bible_fetcher import BibleFetcher, BibleFetchError


class TestBibleFetcherInitialization:
    """Tests for BibleFetcher initialization."""

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    def test_init_default_version(self):
        """Test BibleFetcher initialization with default version."""
        fetcher = BibleFetcher()
        assert fetcher.version == "KJV"

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    def test_init_kjv_version(self):
        """Test BibleFetcher initialization with KJV version."""
        fetcher = BibleFetcher("kjv")
        assert fetcher.version == "KJV"

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    def test_init_asv_version(self):
        """Test BibleFetcher initialization with ASV version."""
        fetcher = BibleFetcher("asv")
        assert fetcher.version == "ASV"

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    def test_init_invalid_version(self):
        """Test BibleFetcher initialization with invalid version."""
        with pytest.raises(BibleFetchError) as exc_info:
            BibleFetcher("NIV")
        assert "Unsupported Bible version: NIV" in str(exc_info.value)

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", False)
    def test_init_no_pythonbible(self):
        """Test BibleFetcher initialization when pythonbible is not available."""
        with pytest.raises(BibleFetchError) as exc_info:
            BibleFetcher()
        assert "pythonbible library is not available" in str(exc_info.value)


class TestBibleFetcherPassageFetching:
    """Tests for fetching Bible passages."""

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    @patch("bible_fetcher.bible")
    def test_fetch_single_verse(self, mock_bible_lib):
        """Test fetching a single Bible verse."""
        mock_bible_lib.get_references.return_value = [Mock()]
        mock_bible_lib.convert_references_to_verse_ids.return_value = [
            1043016
        ]  # John 3:16
        mock_bible_lib.get_verse_text.return_value = "For God so loved the world..."
        mock_bible_lib.get_book_chapter_verse.return_value = (Mock(), 3, 16)
        mock_bible_lib.get_book_titles.return_value = ["John"]
        mock_bible_lib.format_scripture_references.return_value = "John 3:16"
        mock_bible_lib.Version.KING_JAMES = "KJV"

        fetcher = BibleFetcher()
        result = fetcher.fetch_passage("John 3:16")

        assert result["reference"] == "John 3:16"
        assert result["text"] == ["For God so loved the world..."]
        assert result["verses"] == [16]
        assert result["title"] == "John 3"
        assert result["version"] == "KJV"

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    @patch("bible_fetcher.bible")
    def test_fetch_invalid_reference(self, mock_bible_lib):
        """Test fetching with invalid reference."""
        mock_bible_lib.get_references.return_value = []

        fetcher = BibleFetcher()
        with pytest.raises(BibleFetchError) as exc_info:
            fetcher.fetch_passage("Invalid 99:99")

        assert "Invalid Bible reference: Invalid 99:99" in str(exc_info.value)

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", False)
    def test_fetch_no_pythonbible_library(self):
        """Test fetching when pythonbible library is not available."""
        fetcher = BibleFetcher.__new__(BibleFetcher)  # Create without calling __init__
        fetcher.version = "KJV"

        with pytest.raises(BibleFetchError) as exc_info:
            fetcher.fetch_passage("John 3:16")

        assert "pythonbible library is not available" in str(exc_info.value)


class TestBibleFetcherValidation:
    """Tests for reference validation."""

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    @patch("bible_fetcher.bible")
    def test_validate_reference_valid(self, mock_bible_lib):
        """Test validating a valid Bible reference."""
        mock_bible_lib.get_references.return_value = [Mock()]

        fetcher = BibleFetcher()
        result = fetcher.validate_reference("John 3:16")

        assert result is True

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    @patch("bible_fetcher.bible")
    def test_validate_reference_invalid(self, mock_bible_lib):
        """Test validating an invalid Bible reference."""
        mock_bible_lib.get_references.return_value = []

        fetcher = BibleFetcher()
        result = fetcher.validate_reference("Invalid 99:99")

        assert result is False

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", False)
    def test_validate_reference_no_library(self):
        """Test validating reference when library is not available."""
        fetcher = BibleFetcher.__new__(BibleFetcher)  # Create without calling __init__

        result = fetcher.validate_reference("John 3:16")
        assert result is False


class TestBibleFetcherFormatting:
    """Tests for formatting Bible passages."""

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    def test_format_single_verse(self):
        """Test formatting a single verse."""
        fetcher = BibleFetcher()

        passage = {
            "reference": "John 3:16",
            "text": ["For God so loved the world..."],
            "verses": [16],
            "title": "John 3",
            "version": "KJV",
        }

        result = fetcher.format_passage_for_notes(passage)
        assert result == ["For God so loved the world..."]

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    def test_format_multiple_verses_with_numbers(self):
        """Test formatting multiple verses with verse numbers."""
        fetcher = BibleFetcher()

        passage = {
            "reference": "Genesis 1:1-2",
            "text": [
                "In the beginning God created the heaven and the earth.",
                "And the earth was without form, and void...",
            ],
            "verses": [1, 2],
            "title": "Genesis 1",
            "version": "KJV",
        }

        result = fetcher.format_passage_for_notes(passage, include_verse_numbers=True)
        assert result == [
            "1. In the beginning God created the heaven and the earth.",
            "2. And the earth was without form, and void...",
        ]

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    def test_format_passage_with_error(self):
        """Test formatting a passage that contains an error."""
        fetcher = BibleFetcher()

        passage = {
            "reference": "Invalid 99:99",
            "error": "Invalid reference",
            "text": [],
            "verses": [],
            "title": "",
            "version": "KJV",
        }

        with pytest.raises(BibleFetchError) as exc_info:
            fetcher.format_passage_for_notes(passage)

        assert "Invalid reference" in str(exc_info.value)


class TestBibleFetcherMultiplePassages:
    """Tests for fetching multiple passages."""

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    def test_fetch_multiple_passages_success(self):
        """Test fetching multiple passages successfully."""
        fetcher = BibleFetcher()

        # Mock the fetch_passage method
        def mock_fetch_passage(ref):
            return {
                "reference": ref,
                "text": [f"Text for {ref}"],
                "verses": [1],
                "title": f"Title for {ref}",
                "version": "KJV",
            }

        fetcher.fetch_passage = Mock(side_effect=mock_fetch_passage)

        references = ["John 3:16", "Genesis 1:1"]
        results = fetcher.fetch_multiple_passages(references)

        assert len(results) == 2
        for i, result in enumerate(results):
            assert result["reference"] == references[i]
            assert result["text"] == [f"Text for {references[i]}"]

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    def test_fetch_multiple_passages_with_errors(self):
        """Test fetching multiple passages with some errors."""
        fetcher = BibleFetcher()

        def mock_fetch_passage(ref):
            if ref == "Invalid 99:99":
                raise BibleFetchError(f"Invalid reference: {ref}")
            return {
                "reference": ref,
                "text": [f"Text for {ref}"],
                "verses": [1],
                "title": f"Title for {ref}",
                "version": "KJV",
            }

        fetcher.fetch_passage = Mock(side_effect=mock_fetch_passage)

        references = ["John 3:16", "Invalid 99:99"]
        results = fetcher.fetch_multiple_passages(references)

        assert len(results) == 2
        assert "error" not in results[0]  # First passage should succeed
        assert "error" in results[1]  # Second passage should have error
        assert results[1]["error"] == "Invalid reference: Invalid 99:99"


class TestBibleFetcherBooks:
    """Tests for getting available books."""

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    @patch("bible_fetcher.bible")
    def test_get_available_books(self, mock_bible_lib):
        """Test getting available Bible books."""
        # Mock Book enum
        mock_book1 = Mock()
        mock_book2 = Mock()
        mock_bible_lib.Book = [mock_book1, mock_book2]

        mock_bible_lib.get_book_titles.side_effect = [
            ["Genesis", "Gen"],
            ["Exodus", "Exod"],
        ]

        fetcher = BibleFetcher()
        books = fetcher.get_available_books()

        assert books == ["Genesis", "Exodus"]

    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", False)
    def test_get_available_books_no_library(self):
        """Test getting available books when library is not available."""
        fetcher = BibleFetcher.__new__(BibleFetcher)  # Create without calling __init__

        with pytest.raises(BibleFetchError) as exc_info:
            fetcher.get_available_books()

        assert "pythonbible library is not available" in str(exc_info.value)


# Parameterized test data
VALID_REFERENCES = [
    "John 3:16",
    "Genesis 1:1",
    "Psalm 23",
    "Matthew 5:3-12",
]

INVALID_REFERENCES = [
    "Invalid 99:99",
    "NotABook 1:1",
    "",
    "   ",
]


class TestBibleFetcherParameterized:
    """Parameterized tests for BibleFetcher."""

    @pytest.mark.parametrize("reference", VALID_REFERENCES)
    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    @patch("bible_fetcher.bible")
    def test_validate_reference_valid_cases(self, mock_bible_lib, reference):
        """Test validation for various valid references."""
        mock_bible_lib.get_references.return_value = [Mock()]

        fetcher = BibleFetcher()
        result = fetcher.validate_reference(reference)

        assert result is True

    @pytest.mark.parametrize("reference", INVALID_REFERENCES)
    @patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True)
    @patch("bible_fetcher.bible")
    def test_validate_reference_invalid_cases(self, mock_bible_lib, reference):
        """Test validation for various invalid references."""
        mock_bible_lib.get_references.return_value = []

        fetcher = BibleFetcher()
        result = fetcher.validate_reference(reference)

        assert result is False


# Test fixtures
@pytest.fixture
def sample_passage():
    """Sample Bible passage for testing."""
    return {
        "reference": "John 3:16",
        "text": ["For God so loved the world..."],
        "verses": [16],
        "title": "John 3",
        "version": "KJV",
    }


@pytest.fixture
def bible_fetcher():
    """BibleFetcher instance for testing."""
    with patch("bible_fetcher.PYTHONBIBLE_AVAILABLE", True):
        return BibleFetcher()


def test_bible_fetcher_fixture(bible_fetcher):
    """Test that the bible_fetcher fixture works."""
    assert bible_fetcher.version == "KJV"


def test_sample_passage_fixture(sample_passage):
    """Test that the sample_passage fixture works."""
    assert sample_passage["reference"] == "John 3:16"
    assert len(sample_passage["text"]) == 1
