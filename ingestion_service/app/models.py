from .extensions import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)
    # 'metadata' is reserved; use attribute 'event_metadata' mapping to column 'metadata'
    event_metadata = db.Column('metadata', db.JSON, nullable=False)

    def __repr__(self):
        return f'<Event {self.id} {self.event_type}>'