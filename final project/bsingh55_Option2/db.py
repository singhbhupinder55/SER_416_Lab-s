"""
SER 416 – Software Enterprise Projects & Process
Final Project – Option 2 (Developer Route)

Author: Bhupinder Singh (bsingh55)
Date Completed: December 1st 2025

File: db.py
Purpose:
    This module handles all interactions with the SQLite database used
    by the CERT Disaster Preparedness Application. It provides:
        • Database initialization and table creation
        • Insert operations for new household records
        • Query functions for retrieving household data
        • Update functionality for editing existing records

    All persistent storage required by the application flows through
    this module, ensuring a clean separation between business logic
    and data management.

Database:
    The application stores all household readiness information in a
    single SQLite table: households. Each record includes demographic
    data, hazard-related attributes, optional contact details, and
    timestamp metadata.
"""

import sqlite3
from datetime import datetime

# Name of the SQLite database file
DB_NAME = "cert_records.db"


# -----------------------------------------------------------
# CONNECTION MANAGEMENT
# -----------------------------------------------------------
def get_connection():
    """
    Creates and returns a SQLite connection object.
    All other database functions use this helper.
    """
    return sqlite3.connect(DB_NAME)


# -----------------------------------------------------------
# TABLE CREATION
# -----------------------------------------------------------
def create_tables():
    """
    Creates the households table if it does not already exist.

    This function is invoked during program startup to ensure the
    database schema is available before any read/write operations.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS households (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            adults INTEGER NOT NULL,
            children INTEGER NOT NULL,

            has_pets INTEGER NOT NULL,
            has_dogs INTEGER,

            has_critical_meds INTEGER NOT NULL,
            meds_need_fridge INTEGER,

            special_needs TEXT NOT NULL,

            large_propane INTEGER NOT NULL,
            natural_gas INTEGER NOT NULL,

            address TEXT NOT NULL,

            phone TEXT,
            email TEXT,

            has_med_training INTEGER,
            know_neighbors INTEGER,
            has_neighbor_key INTEGER,
            wants_newsletter INTEGER,
            allow_non_disaster_contact INTEGER,

            created_at TEXT,
            updated_at TEXT
        );
    """)

    conn.commit()
    conn.close()


# -----------------------------------------------------------
# INSERTING NEW RECORDS
# -----------------------------------------------------------
def insert_household(data):
    """
    Inserts a new household record into the database.

    Parameters:
        data (dict): A dictionary containing all required and optional
                     household fields collected from user input.

    Automatically adds:
        created_at – timestamp when the record was added
        updated_at – timestamp when the record was last modified
    """
    conn = get_connection()
    cur = conn.cursor()

    fields = (
        "adults", "children", "has_pets", "has_dogs",
        "has_critical_meds", "meds_need_fridge", "special_needs",
        "large_propane", "natural_gas", "address",
        "phone", "email", "has_med_training", "know_neighbors",
        "has_neighbor_key", "wants_newsletter",
        "allow_non_disaster_contact", "created_at", "updated_at"
    )

    # Timestamp values added automatically
    now = datetime.now().isoformat(timespec="seconds")

    # Build values list in exact field order (excluding timestamps)
    values = [data.get(f) for f in fields[:-2]] + [now, now]

    cur.execute(f"""
        INSERT INTO households ({",".join(fields)})
        VALUES ({",".join("?" for _ in fields)});
    """, values)

    conn.commit()
    conn.close()


# -----------------------------------------------------------
# RETRIEVING RECORDS
# -----------------------------------------------------------
def get_all_households():
    """
    Returns a list of all household records in the database.
    Results are sorted by the primary key (id).
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM households ORDER BY id;")
    rows = cur.fetchall()

    conn.close()
    return rows


def get_household_by_id(record_id):
    """
    Retrieves a single household record by its ID.

    Parameters:
        record_id (int): The primary key of the desired household.

    Returns:
        tuple | None: The record row if found, else None.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM households WHERE id = ?;", (record_id,))
    row = cur.fetchone()

    conn.close()
    return row


# -----------------------------------------------------------
# UPDATING EXISTING RECORDS
# -----------------------------------------------------------
def update_household(record_id, data):
    """
    Updates specific fields in an existing household record.

    Parameters:
        record_id (int): ID of the record to update.
        data (dict): A dictionary containing only the fields that
                     should be updated.

    Automatically updates:
        updated_at – timestamp for modification tracking
    """
    conn = get_connection()
    cur = conn.cursor()

    # Always update timestamp
    data["updated_at"] = datetime.now().isoformat(timespec="seconds")

    # Build update clause dynamically based on provided fields
    update_fields = ", ".join(f"{field} = ?" for field in data.keys())
    values = list(data.values()) + [record_id]

    cur.execute(f"""
        UPDATE households
        SET {update_fields}
        WHERE id = ?;
    """, values)

    conn.commit()
    conn.close()