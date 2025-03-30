import psycopg2

DB_CONFIG = {
    "dbname": "tickets",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}


def connect_db():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS events
            (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) UNIQUE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS seats
            (
                id SERIAL PRIMARY KEY,
                seat_name VARCHAR(10) UNIQUE
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets
            (
                id SERIAL PRIMARY KEY,
                ticket_name VARCHAR(100) UNIQUE
            );

        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS events_seats
            (
                id SERIAL PRIMARY KEY,
                event_id INT REFERENCES events(id) ON DELETE CASCADE,
                seat_id INT REFERENCES seats(id) ON DELETE CASCADE 
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS events_tickets
            (
                id SERIAL PRIMARY KEY,
                event_id INT REFERENCES events(id) ON DELETE CASCADE,
                ticket_id INT REFERENCES tickets(id) ON DELETE CASCADE 
            );
        """)


def get_all_events():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM events")

        return cur.fetchall()


def get_all_seats():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM seats")

        return cur.fetchall()

def get_all_tickets():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM tickets")

        return cur.fetchall()


def get_event_info_by_id(event_id):
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        event_info = cur.fetchone()

        cur.execute("""
                SELECT s.seat_name
            FROM events_seats es
                JOIN seats s ON es.seat_id = s.id
            WHERE es.event_id = %s""", (event_id,))

        seats = cur.fetchall()

        cur.execute("""
                SELECT t.ticket_name
            FROM events_tickets et
                JOIN tickets t ON et.ticket_id = t.id
            WHERE et.event_id = %s""", (event_id,))

        tickets = cur.fetchall()
        return {
            "event_info": event_info,
            "seats": seats,
            "tickets": tickets
        }


