from ..services.coring_service import mcp

@mcp.prompt()
def build_opinion_prompt(name,commission_rate,opinion_type):
    return f"""
    Generate opinions about the program based on the following assumptions:
    Program name: {name}
    Commission rate: {commission_rate}
    Opinion type: {opinion_type}
    Rules:
    - Do not change the review type.

    - Do not promise income or guaranteed results.
    - Do not use exaggerated marketing claims.

    Return only the review text."""