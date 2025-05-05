from flask import Blueprint, request, jsonify
import json
from . import task_queue, logger
from .tasks import process_data, process_text
import uuid

bp = Blueprint('main', __name__)

@bp.route('/enqueue', methods=['POST'])
def enqueue_job():
    """
    Endpoint to enqueue a new job for processing
    Expected JSON payload:
    {
        "job_type": "data_processing" or "text_processing",
        "data": {...} or "text content",
        "options": {...} (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        job_type = data.get('job_type')
        if not job_type:
            return jsonify({"error": "job_type is required"}), 400
            
        job_data = data.get('data')
        if job_data is None:
            return jsonify({"error": "data is required"}), 400
            
        options = data.get('options', {})
        
        # Generate a unique job ID
        job_id = str(uuid.uuid4())
        
        # Enqueue the appropriate task based on job_type
        if job_type == "data_processing":
            job = task_queue.enqueue(
                process_data,
                args=(job_data, options),
                job_id=job_id,
                result_ttl=24*3600  # Store the result for 24 hours
            )
        elif job_type == "text_processing":
            job = task_queue.enqueue(
                process_text,
                args=(job_data, options),
                job_id=job_id,
                result_ttl=24*3600
            )
        else:
            return jsonify({"error": f"Unsupported job_type: {job_type}"}), 400
        
        logger.info(f"Job enqueued with ID: {job_id}")
        return jsonify({
            "job_id": job_id,
            "status": "queued",
            "position": len(task_queue)
        }), 202
        
    except Exception as e:
        logger.error(f"Error enqueueing job: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get the status and result of a job"""
    job = task_queue.fetch_job(job_id)
    
    if not job:
        return jsonify({"error": "Job not found"}), 404
        
    status = {
        "job_id": job_id,
        "status": job.get_status(),
        "queue_position": job.get_position() if job.get_position() is not None else 0,
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "ended_at": job.ended_at.isoformat() if job.ended_at else None,
    }
    
    # Add the result if the job is finished
    if job.is_finished:
        status["result"] = job.result
    
    # Add error information if the job failed
    if job.is_failed:
        status["error"] = job.exc_info
    
    return jsonify(status)

@bp.route('/jobs', methods=['GET'])
def list_jobs():
    """List all jobs in the queue"""
    # Get jobs with different statuses
    queued_jobs = task_queue.get_jobs()
    failed_jobs = task_queue.failed_job_registry.get_job_ids()
    completed_jobs = task_queue.finished_job_registry.get_job_ids()
    
    return jsonify({
        "queued_count": len(queued_jobs),
        "failed_count": len(failed_jobs),
        "completed_count": len(completed_jobs),
        "queued_jobs": [{"job_id": job.id, "status": job.get_status()} for job in queued_jobs],
        "failed_jobs": [{"job_id": job_id} for job_id in failed_jobs],
        "completed_jobs": [{"job_id": job_id} for job_id in completed_jobs],
    })
