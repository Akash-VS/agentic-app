from services.gemini_service import ask_gpt

SYNTHESIS_PROMPT = """
You are a senior software debugging architect.

Two independent AI models analyzed the same programming error.

Your task:

1. Compare both analyses carefully.
2. Identify the most technically correct root cause.
3. Remove duplicate information.
4. If both agree → keep the common explanation.
5. If they disagree → choose the more logically consistent explanation.
6. If either response contains hallucinated or irrelevant content → discard it.
7. Ensure the corrected code compiles logically.

Output STRICTLY in this structure:

Root Cause:
<clear explanation>

Fix Suggestion:
<concise actionable fix>

Corrected Code:
<only corrected code block>

Do NOT add extra commentary.
Do NOT repeat analysis sections.
Keep the response concise, technically accurate, and professional.
"""


def merge_debug_responses(resp1: str, resp2: str):

    combined_input = f"""
Model 1 Analysis:
{resp1}

---

Model 2 Analysis:
{resp2}
"""

    final_response = ask_gpt(SYNTHESIS_PROMPT, combined_input)

    return final_response