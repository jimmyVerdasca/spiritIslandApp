def upgrade(cursor):
    cursor.execute(
        """
        ALTER TABLE board_configurations
        ADD COLUMN thematic INTEGER NOT NULL DEFAULT 1
        """
    )