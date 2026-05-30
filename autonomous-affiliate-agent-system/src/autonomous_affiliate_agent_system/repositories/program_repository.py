import sqlite3
from pathlib import Path
from typing import Optional
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

@mcp.tool()
def list_affiliate_programs() -> list[dict]:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, commission_rate, recurring, cookie_duration, final_score"
                   " FROM program_affiliate")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return {'count': 0,"message" : "Brak programów"}
    programs = []
    for row in rows:
        program = dict(row)
        programs.append(program)
    return {"count": len(programs), "programs": programs}

@mcp.tool()
def filter_affiliate_programs(id_program:Optional[int]=None, name_program : Optional[str] = None
                               ,category_program: Optional[str]= None,) -> dict:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query ="SELECT * FROM program_affiliate"
    parms = []
    if id_program is  not None:
        query += " WHERE id = ?"
        parms.append(id_program)
    elif name_program is not None and category_program is not None:
        query += " WHERE name LIKE ? AND category LIKE ?"
        parms.append(f"%{name_program}%")
        parms.append(f"%{category_program}%")
    elif name_program is not None:
        query += " WHERE name LIKE ?"
        parms.append(f"%{name_program}%")
    elif category_program is not None:
        query += " WHERE category LIKE ?"
        parms.append(f"%{category_program}%")
    cursor.execute(query, parms)
    rows = cursor.fetchall()
    conn.close()
    programs = []
    for row in rows:
        program = dict(row)
        programs.append(program)
    return {"count": len(programs), "programs": programs}

