import sys
import os
import json
import time
from datetime import timedelta

# Add the parent directory to the path so we can import app modules
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect.runtime import flow_run
import requests
from app.tasks import process_data, process_text
from app import redis_conn

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def fetch_data_for_processing(source_url, auth_token=None):
    """
    Fetch data from source URL for processing
    """
    headers = {}
    if auth_token:
        headers['Authorization'] = f'Bearer {auth_token}'
    
    response = requests.get(source_url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()

@task
def preprocess_data(data, options=None):
    """
    Apply preprocessing steps to the data
    """
    options = options or {}
    
    # Example preprocessing: filter keys or transform values
    preprocessed = {}
    for key, value in data.items():
        # Skip items we don't want to process
        if options.get('skip_keys') and key in options['skip_keys']:
            continue
        
        # Apply transformations
        if options.get('lowercase_strings') and isinstance(value, str):
            value = value.lower()
            
        preprocessed[key] = value
    
    return preprocessed

@task
def process_data_task(data, options=None):
    """
    Process data with retries and monitoring via Prefect
    """
    # Here we're wrapping our existing process_data function
    return process_data(data, options)

@task
def process_text_task(text, options=None):
    """
    Process text with retries and monitoring via Prefect
    """
    # Here we're wrapping our existing process_text function
    return process_text(text, options)

@task
def save_results(results, destination=None):
    """
    Save processing results to a destination (file, database, etc.)
    """
    if not destination:
        # Default: just print results summary
        print(f"Results: {len(results)} processed items")
        return True
        
    if destination.startswith('file://'):
        # Save to a file
        file_path = destination[7:]  # Remove 'file://' prefix
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=2)
            
    elif destination.startswith('redis://'):
        # Save to Redis
        key = f"results:{int(time.time())}"
        redis_conn.set(key, json.dumps(results))
        print(f"Results saved to Redis key: {key}")
        
    return True

@flow(name="Data Processing Flow")
def data_processing_flow(source_url=None, data=None, options=None, destination=None):
    """
    Complete flow for data processing with Prefect
    
    Can either:
    1. Process provided data directly
    2. Fetch data from source_url first
    
    Results can be saved to a destination
    """
    flow_id = flow_run.id
    print(f"Starting data processing flow: {flow_id}")
    
    options = options or {}
    
    # Step 1: Get the data
    if data is None and source_url:
        auth_token = options.get('auth_token')
        data = fetch_data_for_processing(source_url, auth_token)
    
    if not data:
        raise ValueError("No data provided and no source URL specified")
        
    # Step 2: Preprocess the data
    preprocessed_data = preprocess_data(data, options)
    
    # Step 3: Process the data
    results = process_data_task(preprocessed_data, options)
    
    # Step 4: Save the results if a destination was provided
    if destination:
        save_results(results, destination)
    
    print(f"Data processing flow complete: {flow_id}")
    return results

@flow(name="Text Processing Flow")
def text_processing_flow(source_url=None, text=None, options=None, destination=None):
    """
    Complete flow for text processing with Prefect
    
    Can either:
    1. Process provided text directly
    2. Fetch text from source_url first
    
    Results can be saved to a destination
    """
    flow_id = flow_run.id
    print(f"Starting text processing flow: {flow_id}")
    
    options = options or {}
    
    # Step 1: Get the text
    if text is None and source_url:
        auth_token = options.get('auth_token')
        response = fetch_data_for_processing(source_url, auth_token)
        text = response.get('text', '')
    
    if not text:
        raise ValueError("No text provided and no source URL specified")
        
    # Step 2: Process the text
    results = process_text_task(text, options)
    
    # Step 3: Save the results if a destination was provided
    if destination:
        save_results(results, destination)
    
    print(f"Text processing flow complete: {flow_id}")
    return results

if __name__ == "__main__":
    # Example usage - can be run directly for testing
    # data_processing_flow(data={"sample": "data"}, options={"use_ray": True})
    pass
