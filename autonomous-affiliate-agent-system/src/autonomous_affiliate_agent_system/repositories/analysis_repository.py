import sqlite3
from pathlib import Path
from typing import Optional
from ..services.coring_service import mcp, calculate_final_score, get_opinion_type
from ..agents.affiliate_agents import build_opinion_prompt

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
@mcp.tool()
def create_ai_opinion(id:int):
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT p.commission_rate ,p_a.name, p_a.opinion_type 
    FROM program_analysis AS p_a JOIN program_affiliate AS p ON p_a.affiliate_program_id=p.id 
    WHERE p_a.id = ?""", (id,))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        return f"No program with ID {id}"
    prompt = build_opinion_prompt(row['name'], row['commission_rate'], row['opinion_type'] )
    ai_opin = (prompt)#TU dopisz funkcje wywołania modelu
    cursor.execute("""UPDATE program_analysis SET ai_opinion=? WHERE id=? """, (ai_opin, id))
    conn.commit()
    cursor.close()
    conn.close()
    return f'Opinion generate: {ai_opin}'


def request_analysis_approval(id:int):
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_PATH)
    cursor =conn.cursor()
    while True:
        try:
            sat = int(input("Select 1 to accept, or select 2 to decline: "))
        except ValueError:
            print("Please select 1 or 2")
            continue
        if sat == 1:
            stat = "approved"
            break
        elif sat == 2:
            stat = "declined"
            break
        else:
            print("Select 1 to accept, or select 2 to decline")
    cursor.execute("""UPDATE program_analysis SET status = ? WHERE id = ?""", (stat, id))
    conn.commit()
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return f"No analysis with ID {id}"
    cursor.close()
    conn.close()
    if sat == 1:
        return f"Analysis with ID {id} has been approved"
    elif sat == 2:
        return f"Analysis with ID {id} has been declined"


@mcp.tool()
def request_analysis (id:int):
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""UPDATE program_analysis SET status = ? WHERE id = ?""", ("human_rejected", id))
    conn.commit()
    cursor.close()
    conn.close()
    return f"Analysis with ID {id} Failure of a person to accept"

@mcp.tool()
def get_full_analysis_report(id:int):
    DB_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = DB_DIR / 'data' / 'base.db'
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT  p_a.id AS analysis_id,
            p_a.affiliate_program_id,
            p_a.opinion_type,
            p_a.ai_opinion,
            p_a.status,
            p.name,
            p.category,
            p.commission_rate,
            p.recurring,
            p.cookie_duration,
            p.epc,
            p.final_score FROM program_analysis AS p_a
            JOIN program_affiliate AS p ON p_a.affiliate_program_id = p.id
             WHERE p_a.id = ?""", (id,))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        return f"No analysis with ID {id}"
    cursor.close()
    conn.close()
    analiz = dict(row)
    return analiz


@mcp.tool()
def run_program_analysis_workflow(id:int):
    program = get_program_analysis(id)
    if "error" in program:
        return program["error"]
    analysis_result = add_opinie_type(id)
    opinion_type_result = get_program_analysis(id)
    status =request_analysis(id)
    opinion_result=create_ai_opinion(id)

    return  {"ID": id,
             "analysis_result" : analysis_result,
             "opinion_type_result" : opinion_type_result,
             "opinion_result" : opinion_result,
             "status":status
             }

