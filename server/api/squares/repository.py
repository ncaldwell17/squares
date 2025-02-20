from psycopg2.extensions import connection
from utils.database import get_db_connection
from typing import List
from api.squares.model import Square


class SquaresRepository:

    def __init__(self, conn: connection):
        self.conn = conn
        self.table_name = 'squares'

    def _execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        """Execute a query and return results."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                self.conn.commit()
                if cur.description:  # If the query returns data
                    return cur.fetchall()
                return []
        except Exception as e:
            self.conn.rollback()
            raise

    def add(self, items: List[Square]) -> List[Square]:
        column_names = ['id', 'color', 'rotation']

        # Create placeholders for multiple rows
        placeholders = ','.join([
            f'({",".join(["%s"] * len(column_names))})'
            for _ in items
        ])

        query = f"""
            INSERT INTO {self.table_name} 
            ({','.join(column_names)})
            VALUES {placeholders}
            RETURNING *
        """

        # Flatten the values list for multiple rows
        values = [
            val
            for item in items
            for val in (item.id, item.color, item.rotation)
        ]

        result = self._execute_query(query, values)

        return [
            Square(
                id=record[0],
                color=record[1],
                rotation=record[2]
            )
            for record in result
        ]

    def get_all(self) -> List[Square]:
        query = f"""
            SELECT * FROM {self.table_name}
        """
        result = self._execute_query(query)

        return [
            Square(
                id=record[0],
                color=record[1],
                rotation=record[2]
            )
            for record in result
        ]

    def update(self, items: List[Square]) -> List[Square]:
        query = f"""
            UPDATE {self.table_name}
            SET color = %s, rotation = %s
            WHERE id = %s
            RETURNING *
        """

        # Print the first item's values to debug
        print(f"Updating square with id: {items[0].id}, color: {items[0].color}, rotation: {items[0].rotation}")

        values = [
            (item.color, item.rotation, item.id)
            for item in items
        ][0]  # Since we're only updating one item

        result = self._execute_query(query, values)

        return [
            Square(
                id=record[0],
                color=record[1],
                rotation=record[2]
            )
            for record in result
        ]

    def delete(self) -> None:
        query = f"""
            DELETE FROM {self.table_name}
            RETURNING *
        """
        self._execute_query(query)


if __name__ == "__main__":
    from api.squares.mocks import mock_squares
    import dotenv
    dotenv.load_dotenv()
    db = get_db_connection()
    repo = SquaresRepository(db)
    # repo.add(mock_squares)
    # First check what squares exist
    repo.delete()

