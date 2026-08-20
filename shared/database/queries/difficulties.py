from shared.models.game import Difficulty
from shared.models.converters import row_to_difficulty

def get_all(cursor) -> list[Difficulty]:
    
    cursor.execute(
        """
        SELECT id, level
        FROM difficulties
        ORDER BY level
        """
    )

    return [
        row_to_difficulty(row)
        for row in cursor.fetchall()
    ]



def get_by_level(cursor, level) -> Difficulty | None:
    
    cursor.execute(
        """
        SELECT id, level
        FROM difficulties
        WHERE level = ?
        """,
        (level,)
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return row_to_difficulty(row)