import sqlite3

try:

        conn = sqlite3.connect("task.db")
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
except:
        print("wa")


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
def seeding():
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
    print("Data Inserted in the table: ")
    cur.execute("SELECT * FROM tasks")
    for row in cur.fetchall():
        print(row)
    return row
  
#Delete Rows
def delete():
    result = cur.execute(
        """
        DELETE FROM tasks
        
        """
    )

    conn.commit()
    print("delete")

seeding()

print("DB Name:", table_exist("tasks"))

