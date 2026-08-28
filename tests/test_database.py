from app.db.database import get_connection
from app.db.models import create_tables


def test_database_tables():
    create_tables()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    )

    tables = {row[0] for row in cursor.fetchall()}

    connection.close()

    assert "documents" in tables
    assert "events" in tables