import sqlite3
DB_NAME = "task.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db(conn):
    cur = conn.cursor()

    cur.execute(
            """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        done INTEGER
    );
            """
        )


def table_exist(name):
    result = cur.execute(

        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = ?

        """,(name,)
    ).fetchone()

    return result is not None

#Insert data to the current db
def seeding(conn):
    cur = conn.cursor()
    result = cur.execute(
        """
        INSERT INTO tasks (title, done)
SELECT title, done FROM (
    SELECT 'Buy groceries' AS title, 0 AS done
    UNION ALL SELECT 'Walk the dog', 0
    UNION ALL SELECT 'Read a book', 0
) AS seed_data
WHERE (SELECT COUNT(*) FROM tasks) = 0;

        """
    )
    conn.commit()

#Delete Rows
def delete(conn):
    cur = conn.cursor()
    result = cur.execute(
        """
        DELETE FROM tasks
        """
    )

    conn.commit()
    print("delete")

