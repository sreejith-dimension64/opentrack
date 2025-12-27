"""
Database Migration Script
Populate the face recognition store from your existing RDBMS
"""
import os
from image_store import ImageStore
from typing import List, Dict
import pyodbc
import requests

def example_sqlserver():

    # =========================
    # DB CONNECTION
    # =========================

    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=103.230.85.80,1433;"
        "DATABASE=tnt_dev;"
        "UID=sarvaa;"
        "PWD=Momentiks@123#;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # =========================
    # SQL QUERY
    # =========================

    query = """
        SELECT 
            A.id,
            B.image,
            name,
            email
        FROM Users A
        OUTER APPLY (
            SELECT TOP 1 *
            FROM user_attendance ua
            WHERE 
                ua.user_id = A.Id
                AND ua.image IS NOT NULL
                AND ua.image like 'https://tntstore.blob.core.windows.net/%'
		        AND ua.image NOT like '%sample%'                
            ORDER BY ua.created_date DESC
        ) B
        WHERE 
            A.active_flag = 1 
            AND A.delete_flag = 0
            AND B.image IS NOT NULL
    """

    cursor.execute(query)

    # =========================
    # FETCH + DOWNLOAD IMAGE
    # =========================

    store = ImageStore()    

    for row in cursor.fetchall():
        try:
            user_id = row.id
            image_url = row.image
            name = row.name
            email = row.email

            print(f"User {user_id} -> {image_url}")

            # Download image bytes
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()

            image_bytes = response.content

            success = store.add_image(
                image_bytes=image_bytes,
                user_id=user_id,
                metadata={'name': name, 'email': email}
            )
            if success:
                print(f"✓ Added user {user_id}: {name}")
            else:
                print(f"✗ Failed for user {user_id}: {name}")
        except Exception as e:
            print(f"Error processing user {user_id}: {str(e)}")
            print("Skipping to next user...")

    # =========================
    # CLEANUP
    # =========================

    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("Database Migration Script")
    print("=" * 50)
    print("\nThis script provides templates for populating the face store")
    print("from various data sources. Modify the examples for your setup.")
    print("\nAvailable examples:")
    print("  1. PostgreSQL database")
    print("  2. MySQL database")
    print("  3. Filesystem")
    print("\nUncomment and modify the appropriate function.")
    print("=" * 50)

    example_sqlserver()

