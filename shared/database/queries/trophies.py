GET_ALL = """
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