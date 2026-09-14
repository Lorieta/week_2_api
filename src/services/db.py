import psycopg
import  os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL= os.getenv("DATABASE_URL")


def get_connection():

    return psycopg.connect(DATABASE_URL)

def init_db(conn):
    cur = conn.cursor()

    cur.execute(
            """
 CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    done BOOLEAN DEFAULT FALSE
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
    SELECT 'Buy groceries' AS title, false AS done
    UNION ALL SELECT 'Walk the dog', false 
    UNION ALL SELECT 'Read a book', false 
) AS seed_data
WHERE NOT EXISTS (SELECT 1 FROM tasks);

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

