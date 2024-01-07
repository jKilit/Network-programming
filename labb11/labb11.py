import sqlite3

def import_data_from_file(file_path, conn, c):
    with open(file_path, "r") as file:
        for line in file:
            content = line.strip().split(" ")
            
            # Checkar om the person redan finns i persons table
            c.execute("SELECT id FROM persons WHERE given_name = ? AND second_name = ?;", (content[2], content[3]))
            person_row = c.fetchone()

            if person_row:
                person_id = person_row[0]
            else:
                # om inte, lägg in i person
                c.execute("INSERT INTO persons (given_name, second_name) VALUES (?, ?);", (content[2], content[3]))
                person_id = c.lastrowid

            c.execute('INSERT INTO scores (task_number, points, person_id) VALUES (?, ?, ?)', (int(content[1]), int(content[4]), person_id))

def query_top_persons(conn, c):
    query = """
        SELECT given_name || ' ' || second_name, SUM(points) AS total_points
        FROM scores
        JOIN persons ON persons.id = scores.person_id
        GROUP BY person_id
        ORDER BY total_points DESC
        LIMIT 10;
    """
    return c.execute(query).fetchall()

def query_difficult_tasks(conn, c):
    query = """
        SELECT task_number, SUM(points)
        FROM scores
        GROUP BY task_number
        ORDER BY SUM(points) ASC
        LIMIT 10;
    """
    return c.execute(query).fetchall()

def print_tables(conn, c):    
    print("\nTable: scores")
    for row in c.execute("""
        SELECT persons.given_name, persons.second_name, scores.task_number, scores.points
        FROM scores
        JOIN persons ON persons.id = scores.person_id;
    """):
        print(f"Name: {row[0]} {row[1]}, Task: {row[2]}, Points: {row[3]}")


def database_python():#skapar mina tables
    with sqlite3.connect(":memory:") as conn:
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys = ON')

        c.execute("""
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                given_name TEXT,
                second_name TEXT
            );
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_number INTEGER,
                points INTEGER,
                person_id INTEGER,
                FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
            );
        """)

        import_data_from_file("labb02/score2.txt", conn, c)

        top_persons = query_top_persons(conn, c)
        difficult_tasks = query_difficult_tasks(conn, c)

        print("Top 10 Persons with Highest Total Points:")
        for person, points in top_persons:
            print(f"{person} with {points} points")

        print("Top 10 Most Difficult Tasks:")
        for task, points in difficult_tasks:
            print(f"Task {task} with {points} points")

        print("Do you want to print the generated tables? (yes/no)")
        user_input = input().lower()
        if user_input == 'yes':
            print_tables(conn, c)

if __name__ == "__main__":
    database_python()
