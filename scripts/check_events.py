from app.db.database import get_connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute(
    """
    SELECT id, event_type, document_id, message, created_at
    FROM events
    """
)

events = cursor.fetchall()

for event in events:
    print(event)

connection.close()