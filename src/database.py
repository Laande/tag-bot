import sqlite3

class TagDatabase:
    def __init__(self, db_name="tags.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS tags
                         (user_id INTEGER, tag_name TEXT, content TEXT)''')

    def get_user_tags(self, user_id: int) -> list[str]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tag_name FROM tags WHERE user_id = ?", (user_id,))
            return [row[0] for row in cursor.fetchall()]

    def add_tag(self, user_id: int, tag_name: str, content: str):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO tags VALUES (?, ?, ?)", 
                        (user_id, tag_name, content))

    def update_tag(self, user_id: int, tag_name: str, new_content: str):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("UPDATE tags SET content = ? WHERE user_id = ? AND tag_name = ?",
                        (new_content, user_id, tag_name))

    def delete_tag(self, user_id: int, tag_name: str):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("DELETE FROM tags WHERE user_id = ? AND tag_name = ?",
                        (user_id, tag_name))

    def get_tag_content(self, user_id: int, tag_name: str) -> str | None:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT content FROM tags WHERE user_id = ? AND tag_name = ?",
                          (user_id, tag_name))
            result = cursor.fetchone()
            return result[0] if result else None
        
    def count_tags(self) -> int:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tags")
            return cursor.fetchone()[0]
    
    def count_unique_users(self) -> int:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(DISTINCT user_id) FROM tags")
            return cursor.fetchone()[0]