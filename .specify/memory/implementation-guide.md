# DRY Clean Code Implementation Guide

**Purpose**: Practical examples and patterns for implementing the DRY Clean Code Constitution in Python
**Version**: 1.0.0
**Created**: February 20, 2026

## Immediate Actions Required

Based on codebase analysis, these violations must be addressed immediately:

### 1. Eliminate Code Duplication

**Critical Issue**: Duplicate `TextFilter` classes found
- Location 1: `/src/twins/text_cleaning_job/text_filter.py`
- Location 2: `/twins_ui/components/DUPLICATE_text_filter.py`

**Solution**:
```python
# Create shared library: /src/twins/shared/text_processing.py
from abc import ABC, abstractmethod
from typing import Optional
import re

class TextProcessor(ABC):
    """Abstract base class for text processing operations."""
    
    def __init__(self, max_length: int = -1) -> None:
        self.max_length = max_length
    
    @abstractmethod
    def process(self, text: str) -> str:
        """Process text according to implementation strategy."""
        pass

class StandardTextFilter(TextProcessor):
    """Standard text cleaning implementation."""
    
    def process(self, text: Optional[str]) -> str:
        if not text:
            return ""
        
        cleaned = self._clean_simple(text)
        cleaned = self._remove_xml_tags(cleaned)
        cleaned = self._keep_alphanumeric_characters(cleaned)
        cleaned = self._remove_multi_spaces(cleaned)
        
        return self._apply_length_limit(cleaned)
    
    def _clean_simple(self, text: str) -> str:
        return text.lower().strip()
    
    def _remove_xml_tags(self, text: str) -> str:
        return re.sub(r"<.*?>", "", text)
    
    def _keep_alphanumeric_characters(self, text: str) -> str:
        return re.sub(r"[^a-zA-Z0-9äöüÄÖÜ ]", "", text)
    
    def _remove_multi_spaces(self, text: str) -> str:
        return re.sub(r" {2,}", " ", text).strip()
    
    def _apply_length_limit(self, text: str) -> str:
        if self.max_length > 0:
            return text[:self.max_length]
        return text
```

### 2. Function Parameter Reduction

**Problem**: Functions with too many parameters
```python
# BEFORE (violates principle II)
def main(
    articles: List[dict],
    data_path: Path,
    image_path: Path,
    output_path: Path,
    image_file_ending_format: Callable[[Dict[Any, Any]], str],
    mode: str,
    min_pbk_count=100,
    min_word_count=100,
    train_size=0.95,
    logger=DEFAULT_LOGGER,
):
    # Function body...
```

**Solution**: Use configuration data classes
```python
# AFTER (compliant)
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Callable
import logging

@dataclass(frozen=True)
class ProcessingConfig:
    """Configuration for article preprocessing."""
    data_path: Path
    image_path: Path
    output_path: Path
    image_file_ending_format: Callable[[Dict[Any, Any]], str]
    mode: str
    min_pbk_count: int = 100
    min_word_count: int = 100
    train_size: float = 0.95
    logger: logging.Logger = logging.getLogger(__name__)

def main(articles: List[dict], config: ProcessingConfig) -> None:
    """Process articles according to configuration."""
    # Function body using config.data_path, config.image_path, etc.
```

### 3. Constants and Configuration

**Problem**: Magic numbers and hardcoded values
```python
# BEFORE (violates principle I)
train_size=0.95
min_pbk_count=100
min_word_count=100
```

**Solution**: Centralized configuration
```python
# /src/twins/config/processing_constants.py
from dataclasses import dataclass

@dataclass(frozen=True)
class ProcessingDefaults:
    """Default values for article processing."""
    TRAIN_SIZE: float = 0.95
    MIN_PBK_COUNT: int = 100
    MIN_WORD_COUNT: int = 100
    MAX_TEXT_LENGTH: int = 1000

@dataclass(frozen=True)
class RegexPatterns:
    """Common regex patterns for text processing."""
    HTML_TAGS: str = r"<.*?>"
    NON_ALPHANUMERIC: str = r"[^a-zA-Z0-9äöüÄÖÜ ]"
    MULTI_SPACES: str = r" {2,}"

# Usage in code:
from twins.config.processing_constants import ProcessingDefaults

config = ProcessingConfig(
    train_size=ProcessingDefaults.TRAIN_SIZE,
    # ... other parameters
)
```

## Clean Code Patterns

### 1. Single Responsibility Functions

**Problem**: Functions doing multiple things
```python
# BEFORE (violates principle II)
def clean_all(self, text):
    result = ""
    if text is not None:
        simple_cleaned = self.clean_simple(text)
        without_html = self.remove_xml_tags(simple_cleaned)
        removed_special_chars = self.keep_alphanumeric_characters(without_html)
        result = self.remove_multi_spaces(removed_special_chars)
        if self.max_length > 0:
            result = removed_special_chars[0 : self.max_length]
    return result
```

**Solution**: Composition with single-purpose functions
```python
# AFTER (compliant)
from typing import List, Callable

class TextCleaningPipeline:
    """Composable text cleaning pipeline."""
    
    def __init__(self, max_length: int = -1) -> None:
        self.max_length = max_length
        self._pipeline: List[Callable[[str], str]] = [
            self._clean_simple,
            self._remove_xml_tags,
            self._keep_alphanumeric_characters,
            self._remove_multi_spaces,
        ]
        
        if max_length > 0:
            self._pipeline.append(self._apply_length_limit)
    
    def process(self, text: Optional[str]) -> str:
        if not text:
            return ""
        
        result = text
        for step in self._pipeline:
            result = step(result)
        return result
    
    def _clean_simple(self, text: str) -> str:
        """Convert to lowercase and strip whitespace."""
        return text.lower().strip()
    
    def _remove_xml_tags(self, text: str) -> str:
        """Remove all HTML/XML tags from text."""
        return re.sub(RegexPatterns.HTML_TAGS, "", text)
```

### 2. Type-Safe Error Handling

**Problem**: Generic exception handling
```python
# BEFORE (violates principle IV)
try:
    result = some_operation()
except Exception as e:
    logger.error(f"Error: {e}")
```

**Solution**: Specific exception types
```python
# AFTER (compliant)
from twins.shared.exceptions import (
    ProcessingError,
    InvalidArticleDataError,
    ImageNotFoundError
)

def process_article(article: Dict[str, Any]) -> ProcessedArticle:
    """Process a single article with comprehensive error handling."""
    try:
        validated_article = validate_article_data(article)
    except ValidationError as e:
        raise InvalidArticleDataError(
            f"Article {article.get('id')} validation failed: {e}"
        ) from e
    
    try:
        image_path = get_article_image_path(validated_article.image_id)
    except FileNotFoundError as e:
        raise ImageNotFoundError(
            f"Image not found for article {validated_article.id}: {e}"
        ) from e
    
    return ProcessedArticle(
        data=validated_article,
        image_path=image_path
    )
```

### 3. Dependency Injection

**Problem**: Hard dependencies and testability issues
```python
# BEFORE (violates principle II)
class TextCleaning(beam.DoFn):
    def setup(self):
        self.filter = TextFilter()  # Hard dependency
```

**Solution**: Injectable dependencies
```python
# AFTER (compliant)
from abc import ABC, abstractmethod

class TextProcessor(ABC):
    @abstractmethod
    def process(self, text: str) -> str:
        pass

class TextCleaning(beam.DoFn):
    def __init__(self, text_processor: TextProcessor) -> None:
        self._text_processor = text_processor
    
    def process(self, element: Dict[str, Any]):
        cleaned_text = self._text_processor.process(
            element[Datafields.FIELD_TEXTCORPUS]
        )
        # ... rest of processing

# Factory for production use
def create_text_cleaning_transform() -> TextCleaning:
    processor = StandardTextFilter(max_length=1000)
    return TextCleaning(processor)
```

## Testing Patterns

### 1. Testable Class Design

```python
# Example: Testable text processor
import pytest
from unittest.mock import Mock

class TestStandardTextFilter:
    """Test suite for StandardTextFilter following AAA pattern."""
    
    @pytest.fixture
    def filter_instance(self):
        """Arrange: Create filter instance for testing."""
        return StandardTextFilter(max_length=50)
    
    def test_process_removes_html_tags(self, filter_instance):
        """Test HTML tag removal functionality."""
        # Arrange
        text_with_html = "<p>Hello <b>world</b></p>"
        expected = "hello world"
        
        # Act
        result = filter_instance.process(text_with_html)
        
        # Assert
        assert result == expected
    
    def test_process_handles_none_input(self, filter_instance):
        """Test graceful handling of None input."""
        # Arrange
        text_input = None
        expected = ""
        
        # Act
        result = filter_instance.process(text_input)
        
        # Assert
        assert result == expected
    
    def test_process_applies_length_limit(self, filter_instance):
        """Test length limiting functionality."""
        # Arrange
        long_text = "a" * 100
        expected_length = 50
        
        # Act
        result = filter_instance.process(long_text)
        
        # Assert
        assert len(result) == expected_length
```

### 2. Integration Testing

```python
# Example: Integration test for text processing pipeline
import tempfile
from pathlib import Path

class TestTextProcessingIntegration:
    """Integration tests for the complete text processing workflow."""
    
    def test_end_to_end_text_processing(self):
        """Test complete pipeline from input to output."""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.json"
            output_path = Path(temp_dir) / "output"
            
            test_articles = [
                {"id": "1", "text": "<p>Test article</p>"},
                {"id": "2", "text": "Another test!!"}
            ]
            
            config = ProcessingConfig(
                input_path=input_path,
                output_path=output_path,
                processor=StandardTextFilter()
            )
            
            # Act
            pipeline = TextProcessingPipeline(config)
            results = pipeline.process_articles(test_articles)
            
            # Assert
            assert len(results) == 2
            assert results[0]["text"] == "test article"
            assert results[1]["text"] == "another test"
```

## Migration Strategy

### Phase 1: Immediate Fixes (Week 1)
1. **Remove duplicate `TextFilter`** - Consolidate into shared library
2. **Extract constants** - Move all magic numbers to configuration classes  
3. **Add type annotations** - Add types to all public interfaces

### Phase 2: Function Refactoring (Week 2-3)
1. **Break down large functions** - Split functions > 20 lines
2. **Reduce parameter counts** - Convert to configuration objects
3. **Add comprehensive tests** - Achieve 80% coverage

### Phase 3: Architecture Improvements (Week 4-6)
1. **Implement dependency injection** - Remove hard dependencies
2. **Create domain boundaries** - Reorganize packages by domain
3. **Add integration tests** - Test external dependencies

## Tools and Automation

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
        language_version: python3.11
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88', '--extend-ignore=E203']
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

### CI/CD Integration
```yaml
# .github/workflows/code-quality.yml
name: Code Quality
on: [push, pull_request]
jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install pylint mypy bandit pytest-cov
      
      - name: Run static analysis
        run: |
          pylint src/
          mypy src/
          bandit -r src/
      
      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=xml --cov-fail-under=80
```

---

**Remember**: This constitution is not just about writing better code—it's about creating a sustainable, maintainable codebase that enables long-term success. Every developer is responsible for upholding these standards.