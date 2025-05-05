import time
import json
import logging
from . import logger
from .ray_cluster import run_distributed_task

def process_data(data, options=None):
    """
    Process structured data using distributed computing with Ray
    
    Args:
        data: Dictionary containing the data to process
        options: Dictionary with processing options
        
    Returns:
        Dictionary with processing results
    """
    logger.info(f"Processing data job with options: {options}")
    options = options or {}
    
    # Extract processing parameters
    batch_size = options.get('batch_size', 10)
    use_ray = options.get('use_ray', True)
    
    try:
        # Simulate some initial data validation/preprocessing
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
            
        # Log the start of processing
        start_time = time.time()
        logger.info(f"Starting data processing job with {len(data)} items")
        
        results = {}
        
        if use_ray:
            # Use Ray for distributed processing
            logger.info("Using Ray for distributed processing")
            results = run_distributed_task(
                task_type="data_processing",
                data=data,
                batch_size=batch_size
            )
        else:
            # Simple sequential processing
            logger.info("Using sequential processing")
            # Simulate processing each key-value pair
            for key, value in data.items():
                # Simulate processing work
                time.sleep(0.1)
                results[key] = f"Processed: {value}"
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Prepare the result
        result = {
            "status": "success",
            "processing_time": processing_time,
            "items_processed": len(data),
            "results": results
        }
        
        logger.info(f"Data processing completed in {processing_time:.2f} seconds")
        return result
        
    except Exception as e:
        logger.error(f"Error in data processing: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

def process_text(text, options=None):
    """
    Process text data with NLP-like operations
    
    Args:
        text: String containing the text to process
        options: Dictionary with processing options
        
    Returns:
        Dictionary with processing results
    """
    logger.info(f"Processing text job with options: {options}")
    options = options or {}
    
    # Extract processing parameters
    operations = options.get('operations', ['count', 'tokenize'])
    use_ray = options.get('use_ray', True)
    
    try:
        # Validate input
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
            
        # Log the start of processing
        start_time = time.time()
        logger.info(f"Starting text processing job with {len(text)} characters")
        
        results = {}
        
        if use_ray and len(text) > 1000:
            # Use Ray for distributed processing of larger text
            logger.info("Using Ray for distributed text processing")
            results = run_distributed_task(
                task_type="text_processing",
                data=text,
                operations=operations
            )
        else:
            # Simple sequential processing
            logger.info("Using sequential processing")
            
            # Perform requested operations
            if 'count' in operations:
                # Count words and characters
                words = text.split()
                results['word_count'] = len(words)
                results['char_count'] = len(text)
                
            if 'tokenize' in operations:
                # Simple tokenization (in real app, would use an NLP library)
                results['tokens'] = text.split()[:100]  # Limit output tokens
                results['unique_tokens'] = list(set(text.lower().split()))[:100]
                
            if 'sentiment' in operations:
                # Simulate sentiment analysis
                # (would use a real NLP model in production)
                positive_words = ['good', 'great', 'excellent', 'best', 'happy']
                negative_words = ['bad', 'worst', 'poor', 'terrible', 'sad']
                
                words = text.lower().split()
                pos_count = sum(1 for word in words if word in positive_words)
                neg_count = sum(1 for word in words if word in negative_words)
                
                if pos_count > neg_count:
                    sentiment = "positive"
                elif neg_count > pos_count:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
                    
                results['sentiment'] = {
                    'label': sentiment,
                    'positive_words': pos_count,
                    'negative_words': neg_count
                }
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Prepare the result
        result = {
            "status": "success",
            "processing_time": processing_time,
            "text_length": len(text),
            "results": results
        }
        
        logger.info(f"Text processing completed in {processing_time:.2f} seconds")
        return result
        
    except Exception as e:
        logger.error(f"Error in text processing: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }
