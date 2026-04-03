from database.connection import DatabaseConnection


def init_database() -> None:
    """Initialize database schema"""

    schema = """
    CREATE TABLE IF NOT EXISTS transactions (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL CHECK(type IN ('debit', 'credit', 'entry')),
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS balance (
        id INTEGER PRIMARY KEY,
        amount REAL NOT NULL DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS fixed_expenses (
        id TEXT PRIMARY KEY,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        created_date TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS installments (
        id TEXT PRIMARY KEY,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        total_installments INTEGER NOT NULL,
        paid_installments INTEGER NOT NULL DEFAULT 0,
        created_date TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS invoices (
        id TEXT PRIMARY KEY,
        closing_day INTEGER NOT NULL DEFAULT 5,
        due_day INTEGER NOT NULL DEFAULT 12,
        status TEXT NOT NULL CHECK(status IN ('open', 'closed', 'paid')) DEFAULT 'open',
        total REAL NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS invoice_items (
        id TEXT PRIMARY KEY,
        invoice_id TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS reminders (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL CHECK(type IN ('fixed', 'installment', 'standalone')),
        linked_id TEXT NOT NULL,
        days_before INTEGER NOT NULL,
        message TEXT,
        created_date TEXT NOT NULL
    );
    """

    with DatabaseConnection.get_connection() as conn:
        cursor = conn.cursor()

        # Split and execute each statement separately
        for statement in schema.split(";"):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)

        # Initialize balance if not exists
        cursor.execute("SELECT COUNT(*) FROM balance")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO balance (amount) VALUES (0)")

        conn.commit()


if __name__ == "__main__":
    init_database()
    print("✅ Database initialized successfully")
