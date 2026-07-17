import os
import sqlite3
from dotenv import load_dotenv

load_dotenv(".env.development")

DB_TYPE = os.getenv("DB_TYPE")


def get_connection():

    if DB_TYPE == "sqlite":
        conn = sqlite3.connect(os.getenv("DB_PATH"))
        conn.row_factory = sqlite3.Row
        return conn

    elif DB_TYPE == "mysql":
        import mysql.connector

        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        return conn

    else:
        raise Exception("Invalid database type.")