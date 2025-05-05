import pytest
import json
from app.tasks import process_data, process_text

class TestTasks:
    def test_process_data(self):
        """Test data processing functionality"""
        # Test data
        test_data = {
            "item1": "value1",
            "item2": "value2"
        }
        
        # Process without Ray
        result = process_data(test_data, {"use_ray": False})
        
        # Assertions
        assert result["status"] == "success"
        assert "processing_time" in result
        assert result["items_processed"] == 2
        assert "results" in result
        assert len(result["results"]) == 2
        
    def test_process_data_invalid_input(self):
        """Test data processing with invalid input"""
        # Test with non-dict input
        result = process_data("not a dict")
        
        # Should return error status
        assert result["status"] == "error"
        assert "error" in result
    
    def test_process_text(self):
        """Test text processing functionality"""
        # Test text
        test_text = "This is a sample text for processing. It contains multiple words for testing."
        
        # Process with counting and tokenization
        result = process_text(test_text, {"operations": ["count", "tokenize"], "use_ray": False})
        
        # Assertions
        assert result["status"] == "success"
        assert "processing_time" in result
        assert result["text_length"] == len(test_text)
        assert "results" in result
        assert "word_count" in result["results"]
        assert result["results"]["word_count"] == len(test_text.split())
        assert "tokens" in result["results"]
    
    def test_process_text_sentiment(self):
        """Test text sentiment analysis"""
        # Positive text
        positive_text = "This is good and excellent. I am happy with the great results."
        
        # Process with sentiment analysis
        result = process_text(positive_text, {"operations": ["sentiment"], "use_ray": False})
        
        # Assertions
        assert result["status"] == "success"
        assert "results" in result
        assert "sentiment" in result["results"]
        assert result["results"]["sentiment"]["label"] == "positive"
        
        # Negative text
        negative_text = "This is bad and terrible. I am sad with the poor results."
        
        # Process with sentiment analysis
        result = process_text(negative_text, {"operations": ["sentiment"], "use_ray": False})
        
        # Assertions
        assert result["status"] == "success"
        assert "results" in result
        assert "sentiment" in result["results"]
        assert result["results"]["sentiment"]["label"] == "negative"
