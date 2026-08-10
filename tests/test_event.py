from app.db.events import log_event


log_event(
    event_type="DOCUMENT_LOADED",
    document_id="DOC001",
    message="Document loaded successfully",
)

print("Event logged successfully.")