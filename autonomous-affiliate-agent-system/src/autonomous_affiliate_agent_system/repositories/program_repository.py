import sqlite3
from pathlib import Path
from typing import Optional
from ..services.coring_service import mcp


def create_program_analysis(id):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM  program_affiliate WHERE id = ?",(id,))
    row = cursor.fetchone()
    cursor.execute("INSERT INTO program_analysis (affiliate_program_id), (name) VALUES (?,?)",
                   (id,row[0],))
    conn.commit()
    cursor.close()
    conn.close()
    return f"program analysis added with ID {id}"


@mcp.tool()
def get_affiliate_program(id_program:int) -> dict:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM program_affiliate WHERE id =?", (id_program,))

    row = cursor.fetchone()
    cursor.close()
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
    cursor.close()
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
    cursor.close()
    conn.close()
    programs = []
    for row in rows:
        program = dict(row)
        programs.append(program)
    return {"count": len(programs), "programs": programs}

@mcp.tool()
def update_affiliate_programs(id_program: int,name_program : Optional[str] = None
                               ,category_program: Optional[str]= None, commission_rate_program: Optional[str] = None,
                                recurring_program: Optional[bool] = None,cookie_duration_program: Optional[str] = None,
                                epc_program: Optional[float] = None):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM program_affiliate WHERE id = ?", (id_program,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        cursor.close()
        return f"No program with ID {id_program}"
    fields = {}
    if name_program is not None:
        fields["name"] = name_program
    if category_program is not None:
        fields["category"] = category_program
    if commission_rate_program is not None:
        fields["commission_rate"] = commission_rate_program
    if recurring_program is not None:
        fields["recurring"] = recurring_program
    if cookie_duration_program is not None:
        fields["cookie_duration"] = cookie_duration_program
    if epc_program is not None:
        fields["epc"] = epc_program
    if not fields:
        cursor.close()
        conn.close()
        return "No parameters"
    set_clouse = ", ".join([f"{fild}=?" for fild in fields.keys()])
    value= list(fields.values())
    value.append(id_program)
    cursor.execute(f"""UPDATE program_affiliate SET {set_clouse} WHERE id = ?""", value)
    conn.commit()
    cursor.close()
    conn.close()
    return f"The ID{id_program} program has been updated"

