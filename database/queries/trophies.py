from models.converters import row_to_trophy


def get_all(cursor):

    cursor.execute(
        """
        SELECT
            id,
            key,
            locked_image,
            unlocked_image,
            sql_condition,
            python_condition

        FROM trophies

        ORDER BY id
        """
    )

    return [
        row_to_trophy(row)
        for row in cursor.fetchall()
    ]