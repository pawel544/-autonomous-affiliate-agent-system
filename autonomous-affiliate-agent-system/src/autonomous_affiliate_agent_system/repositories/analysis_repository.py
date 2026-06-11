import sqlite3
from pathlib import Path
from typing import Optional
from ..services.coring_service import mcp, calculate_final_score, get_opinion_type


@mcp.tool()
def add_opinie_type(id:int):
    calculate_final_score(id)
    a = get_opinion_type(id)
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""UPDATE program_analysis SET opinion_type=? WHERE affiliate_program_id = ?""", (a, id))
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return f"No program with ID {id}"
    conn.commit()
    cursor.close()
    conn.close()
    return "success"

@mcp.tool()
def get_program_analysis(id:int):
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT p_a.affiliate_program_id,  p_a.opinion_type, p_a.ai_opinion, p.final_score 
    FROM program_analysis AS p_a JOIN program_affiliate AS p ON p_a.affiliate_program_id=p.id 
    WHERE p_a.id = ?""", (id,))
    rows = cursor.fetchone()
    if rows is None:
        cursor.close()
        conn.close()
        return f"No program with ID {id}"

    program = dict(rows)
    cursor.close()
    conn.close()
    return program
