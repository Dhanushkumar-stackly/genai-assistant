from datetime import datetime, UTC

from app.db.database import get_connection


def log_event(
    event_type: str,
    document_id: str | None,
    message: str,
) -> None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO events (
            event_type,
            document_id,
            message,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            event_type,
            document_id,
            message,
            datetime.now(UTC).isoformat(),
        ),
    )

    connection.commit()
    connection.close()