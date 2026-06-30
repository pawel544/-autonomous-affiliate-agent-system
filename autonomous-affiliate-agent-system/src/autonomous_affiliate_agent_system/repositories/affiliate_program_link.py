import sqlite3
from pathlib import Path
from typing import Optional
from ..services.coring_service import mcp

@mcp.tool()
def add_link(link):
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Connection (link) VALUES (?)""", (link,))
    conn.commit()
    cursor.close()
    conn.close()
    return "added link"

@mcp.tool()
def show_all_links():
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / 'data' / "base.db"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Connection")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if not rows:
        return {"count": 0 , "message": "No links"}
    link= []
    for row in rows:
        links = dict(row)
        link.append(links)
        return {"count": len(link), "links": link}

@mcp.tool()
def update_link(link,id):
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""UPDATE Connection SET link = ? WHERE id = ?""",(link, id))
    conn.commit()
    cursor.close()
    conn.close()
    return "updated link"

@mcp.tool()
def delete_link(id):
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'
    conn= sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM Connection WHERE id = ?""", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return "deleted link"