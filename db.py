"""This file is responsible for connecting the application to the database."""

import os
import sqlite3
from typing import Any
import mysql.connector
from dotenv import load_dotenv

load_dotenv(".env.development")

DB_TYPE = os.getenv("DB_TYPE")


def get_connection() -> Any:
    """Create and return a connection to the selected database."""
    if DB_TYPE == "sqlite":
        conn = sqlite3.connect(os.getenv("DB_PATH"))
        conn.row_factory = sqlite3.Row
        return conn

    if DB_TYPE == "mysql":

        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        return conn

    raise ValueError("Invalid database type.")
