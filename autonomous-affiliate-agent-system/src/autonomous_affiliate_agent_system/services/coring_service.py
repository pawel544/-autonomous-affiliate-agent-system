import sqlite3
from pathlib import Path

from mcp.server import FastMCP

mcp= FastMCP(name="DataTools", host="0.0.0.0", port=8080)

@mcp.tool()
def add_affiliate_program(name: str, category: str,commission_rate: str | None= None,
                          recurring: bool= False, cookie_duration: str | None=None,
                          epc: float | None = None):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    DB_FILE = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO program_affiliate (name,"
                   "category,commission_rate,recurring,"
                   "cookie_duration,epc) VALUES (?,?,?,?,?,?)",
                   (name,category,commission_rate,recurring,cookie_duration,epc))
    conn.commit()
    program_id= cursor.lastrowid
    #TU BĘDZIE WYWOŁANIE PROMPTA WY WYLICZENIA!!
    conn.close()
    return f" Program dodany o numerze {program_id} id"



def get_opinion_type(id_program:int) ->str:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    DB_FILE = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT final_score FROM  program_affiliate WHERE id =?" ,(id_program,))
    row = cursor.fetchone()
    conn.close()
    if  row is not None:
        final_score=row[0]
        if final_score >=70:

            return "Pozitiw"
        elif 40 <= final_score < 70:

            return "Neutral"
        else:

            return "Negativ"
    else:
        return "WE NEED MORE INFO!!"

print(get_opinion_type(50))

def calculate_final_score( id_program: int) -> float:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
    DB_FILE = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT reputation_score,seo_potential_score,competition_score"
                   " FROM program_affiliate WHERE id = ?", (id_program,))
    row = cursor.fetchone()
    score =( row[0] * 0.30 + row[1] * 0.40 + row[2] * 0.30) *10
    score= round(score,2)
    cursor.execute("UPDATE program_affiliate SET final_score= ? WHERE id = ? ",(score,id_program))
    conn.commit()
    conn.close()
    return score