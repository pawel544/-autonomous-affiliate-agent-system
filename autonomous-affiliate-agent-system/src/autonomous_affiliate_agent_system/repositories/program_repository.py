import sqlite3
from pathlib import Path
from ..services.coring_service import mcp

@mcp.tool()
def get_affiliate_program(id_program:int) -> dict:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM program_affiliate WHERE id =?", (id_program,))

    row = cursor.fetchone()
    conn.close()
    if row is None:
        return {"error": f"Brak programu o ID {id_program} "}
    program = dict(row)
    return program