import sqlite3
import os
from datetime import datetime
from typing import Optional
from pathlib import Path


class ResourcePersistence:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.publishers_db = self.data_dir / "qa_publishers.db"
        self.environments_db = self.data_dir / "staging_environments.db"

        self._init_databases()

    def _init_databases(self):
        """Initialize the database tables if they don't exist."""
        # Initialize publishers database
        with sqlite3.connect(self.publishers_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS resource_state (
                    resource_id TEXT PRIMARY KEY,
                    taken_by TEXT,
                    taken_at TEXT,
                    last_updated TEXT
                )
            """)
            conn.commit()

        # Initialize environments database
        with sqlite3.connect(self.environments_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS resource_state (
                    resource_id TEXT PRIMARY KEY,
                    taken_by TEXT,
                    taken_at TEXT,
                    last_updated TEXT
                )
            """)
            conn.commit()

    def save_state(self, resources_registry) -> None:
        """Save the current state of all resources to SQLite databases."""
        try:
            # Save publishers to qa_publishers.db
            with sqlite3.connect(self.publishers_db) as conn:
                for pub_id, publisher in resources_registry.publishers.items():
                    conn.execute("""
                        INSERT OR REPLACE INTO resource_state
                        (resource_id, taken_by, taken_at, last_updated)
                        VALUES (?, ?, ?, ?)
                    """, (
                        pub_id,
                        publisher.taken_by,
                        publisher.taken_at.isoformat() if publisher.taken_at else None,
                        datetime.now().isoformat()
                    ))
                conn.commit()

            # Save environments to staging_environments.db
            with sqlite3.connect(self.environments_db) as conn:
                for env_id, environment in resources_registry.environments.items():
                    conn.execute("""
                        INSERT OR REPLACE INTO resource_state
                        (resource_id, taken_by, taken_at, last_updated)
                        VALUES (?, ?, ?, ?)
                    """, (
                        env_id,
                        environment.taken_by,
                        environment.taken_at.isoformat() if environment.taken_at else None,
                        datetime.now().isoformat()
                    ))
                conn.commit()

        except Exception as e:
            print(f"Error saving state: {e}")
            import traceback
            traceback.print_exc()

    def load_state(self, resources_registry) -> bool:
        """Load the saved state from SQLite databases and apply it to the resources registry."""
        try:
            loaded_any = False

            # Load publishers from qa_publishers.db
            if self.publishers_db.exists():
                with sqlite3.connect(self.publishers_db) as conn:
                    cursor = conn.execute("SELECT resource_id, taken_by, taken_at FROM resource_state")
                    for row in cursor:
                        resource_id, taken_by, taken_at_str = row
                        if resource_id in resources_registry.publishers:
                            publisher = resources_registry.publishers[resource_id]
                            publisher.taken_by = taken_by
                            publisher.taken_at = datetime.fromisoformat(taken_at_str) if taken_at_str else None
                            loaded_any = True

            # Load environments from staging_environments.db
            if self.environments_db.exists():
                with sqlite3.connect(self.environments_db) as conn:
                    cursor = conn.execute("SELECT resource_id, taken_by, taken_at FROM resource_state")
                    for row in cursor:
                        resource_id, taken_by, taken_at_str = row
                        if resource_id in resources_registry.environments:
                            environment = resources_registry.environments[resource_id]
                            environment.taken_by = taken_by
                            environment.taken_at = datetime.fromisoformat(taken_at_str) if taken_at_str else None
                            loaded_any = True

            return loaded_any

        except Exception as e:
            print(f"Error loading state: {e}")
            import traceback
            traceback.print_exc()
            return False

    def clear_state(self) -> None:
        """Clear all persisted state by deleting the database files."""
        if self.publishers_db.exists():
            self.publishers_db.unlink()
        if self.environments_db.exists():
            self.environments_db.unlink()
