import sqlite3
from pathlib import Path
from typing import Optional
from ..services.coring_service import mcp, calculate_final_score, get_opinion_type


@mcp.tool()
def add_opinie_type(id:int):
    calculate_final_score(id)
    a = get_opinion_type(id)
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / 'data' / 'db.sqlite3'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""UPDATE program_analysis SET opinion_type=? WHERE id = ?""", (a, id))
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return f"No program with ID {id}"
    conn.commit()
    cursor.close()
    conn.close()
    return "success"