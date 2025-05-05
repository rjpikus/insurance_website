import time
import logging
import ray
from . import logger
from .config import RAY_ADDRESS, RAY_NUM_CPUS

# Initialize Ray when this module is imported
try:
    ray.init(address=RAY_ADDRESS, num_cpus=RAY_NUM_CPUS, ignore_reinit_error=True)
    logger.info(f"Ray initialized with {RAY_NUM_CPUS} CPUs")
except Exception as e:
    logger.warning(f"Failed to initialize Ray: {str(e)}. Will use local execution.")

@ray.remote
def process_data_chunk(chunk, operation=None):
    """
    Ray task for processing a chunk of data
    
    Args:
        chunk: A subset of data to process
        operation: Optional operation name to perform
        
    Returns:
        Processed chunk results
    """
    # Simulate processing work with a small delay
    time.sleep(0.1 * len(chunk))
    
    result = {}
    # Process each item in the chunk
    for key, value in chunk.items():
        # This is a simplified simulation - in a real application
        # we'd have more complex data transformation logic here
        result[key] = f"Processed {operation if operation else 'standard'}: {value}"
        
    return result

@ray.remote
def process_text_chunk(chunk, operations=None):
    """
    Ray task for processing a chunk of text
    
    Args:
        chunk: A substring of text to process
        operations: List of operations to perform
        
    Returns:
        Dictionary with processing results for this chunk
    """
    operations = operations or ['count']
    results = {}
    
    # Simulate processing with a small delay
    time.sleep(0.05)
    
    # Count words and characters
    if 'count' in operations:
        words = chunk.split()
        results['word_count'] = len(words)
        results['char_count'] = len(chunk)
    
    # Simple tokenization
    if 'tokenize' in operations:
        results['tokens'] = chunk.split()
        
    return results

def run_distributed_task(task_type, data, **kwargs):
    """
    Run a task distributed across Ray workers
    
    Args:
        task_type: Type of task ('data_processing' or 'text_processing')
        data: The data to process
        **kwargs: Additional task-specific parameters
        
    Returns:
        Dictionary with combined results from all workers
    """
    if not ray.is_initialized():
        try:
            ray.init(address=RAY_ADDRESS, num_cpus=RAY_NUM_CPUS, ignore_reinit_error=True)
            logger.info(f"Ray initialized with {RAY_NUM_CPUS} CPUs")
        except Exception as e:
            logger.error(f"Failed to initialize Ray: {str(e)}. Falling back to local execution.")
            # Provide a minimal fallback implementation based on task type
            if task_type == "data_processing":
                result = {}
                for key, value in data.items():
                    result[key] = f"Locally processed: {value}"
                return result
            elif task_type == "text_processing":
                operations = kwargs.get('operations', ['count'])
                result = {}
                if 'count' in operations:
                    words = data.split()
                    result['word_count'] = len(words)
                    result['char_count'] = len(data)
                if 'tokenize' in operations:
                    result['tokens'] = data.split()[:100]
                return result
    
    try:
        start_time = time.time()
        
        if task_type == "data_processing":
            # For data processing, we partition the dictionary
            batch_size = kwargs.get('batch_size', 10)
            
            # Divide data into chunks
            chunks = []
            current_chunk = {}
            for i, (key, value) in enumerate(data.items()):
                current_chunk[key] = value
                if (i + 1) % batch_size == 0:
                    chunks.append(current_chunk)
                    current_chunk = {}
            
            # Add any remaining items
            if current_chunk:
                chunks.append(current_chunk)
            
            # Process chunks in parallel
            operation = kwargs.get('operation')
            logger.info(f"Submitting {len(chunks)} data chunks to Ray cluster")
            futures = [process_data_chunk.remote(chunk, operation) for chunk in chunks]
            chunk_results = ray.get(futures)
            
            # Combine results from all chunks
            result = {}
            for chunk_result in chunk_results:
                result.update(chunk_result)
            
        elif task_type == "text_processing":
            # For text processing, we split the text into chunks
            text = data
            chunk_size = kwargs.get('chunk_size', 1000)  # Default 1000 characters per chunk
            operations = kwargs.get('operations', ['count'])
            
            # Split text into chunks of approximately chunk_size
            if len(text) <= chunk_size:
                text_chunks = [text]
            else:
                # Split at whitespace boundaries around the chunk_size
                text_chunks = []
                start = 0
                while start < len(text):
                    end = min(start + chunk_size, len(text))
                    # If we're not at the end and not at a whitespace, back up to find whitespace
                    if end < len(text) and not text[end].isspace():
                        # Find previous whitespace
                        while end > start and not text[end].isspace():
                            end -= 1
                        # If we backed up all the way to start, just use the original end
                        if end == start:
                            end = min(start + chunk_size, len(text))
                    
                    text_chunks.append(text[start:end])
                    start = end
            
            # Process chunks in parallel
            logger.info(f"Submitting {len(text_chunks)} text chunks to Ray cluster")
            futures = [process_text_chunk.remote(chunk, operations) for chunk in text_chunks]
            chunk_results = ray.get(futures)
            
            # Combine results from all chunks
            if 'count' in operations:
                word_count = sum(cr.get('word_count', 0) for cr in chunk_results)
                char_count = sum(cr.get('char_count', 0) for cr in chunk_results)
                result = {
                    'word_count': word_count,
                    'char_count': char_count,
                }
            
            if 'tokenize' in operations:
                all_tokens = []
                for cr in chunk_results:
                    if 'tokens' in cr:
                        all_tokens.extend(cr['tokens'])
                # Limit the number of tokens returned to avoid huge responses
                result['tokens'] = all_tokens[:100]
                result['unique_tokens'] = list(set(all_tokens))[:100]
            
        else:
            raise ValueError(f"Unsupported task type: {task_type}")
        
        processing_time = time.time() - start_time
        logger.info(f"Ray distributed processing completed in {processing_time:.2f} seconds")
        
        return result
    
    except Exception as e:
        logger.error(f"Error in Ray distributed task: {str(e)}")
        return {"error": str(e)}
