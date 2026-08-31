GET_ALL = """
    SELECT
        id,
        level

    FROM difficulties

    ORDER BY level
"""


GET_BY_LEVEL = """
    SELECT
        id,
        level

    FROM difficulties

    WHERE level = ?
"""