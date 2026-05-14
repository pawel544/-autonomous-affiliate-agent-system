import sqlite3
from pathlib import Path

def get_opinion_type(id_program:int) ->str:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
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

print(get_opinion_type(1))