from flask import Blueprint, request, jsonify, render_template_string
from . import db, logger
from .models import Event
from .extensions import redis_client

bp = Blueprint('routes', __name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Page Views</title></head>
<body>
    <h1>This page has been viewed {{ count }} times.</h1>
</body>
</html>
"""

@bp.route("/views")
def view_counter():
    count = redis_client.incr("page_views")
    return render_template_string(HTML_TEMPLATE, count=count)


@bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@bp.route('/events', methods=['POST'])
def post_events():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    events = data if isinstance(data, list) else [data]
    inserted = []
    for evt in events:
        try:
            e = Event(
                event_type=evt['event_type'],
                timestamp=evt['timestamp'],
                event_metadata=evt.get('metadata', {})
            )
            db.session.add(e)
            inserted.append(evt)
        except KeyError:
            return jsonify({'error': 'Missing fields in event'}), 400
    db.session.commit()
    logger.info(f'Inserted {len(inserted)} event(s)')
    return jsonify({'inserted': len(inserted)}), 200

@bp.route('/events', methods=['GET'])
def get_events():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    evts = Event.query.paginate(page=page, per_page=per_page, error_out=False)
    items = [
        {
            'id': e.id,
            'event_type': e.event_type,
            'timestamp': e.timestamp,
            'metadata': e.event_metadata
        }
        for e in evts.items
    ]
    return jsonify({'events': items}), 200
