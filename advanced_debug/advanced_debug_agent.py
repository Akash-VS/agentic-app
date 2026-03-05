import asyncio
from .openrouter_service import ask_openrouter
from .response_merger import merge_debug_responses
from config import DEBUG_MODEL_1, DEBUG_MODEL_2


SYSTEM_PROMPT = """
You are a senior debugging expert.
You are a senior debugging expert with 20 years of experience in backend, API's frontend, DevOps, and production systems.
over the years,
you have extensive experience in identifying and fixing bugs in various programming languages and frameworks.
Given an error:
You are a senior debugging expert with 20 years of experience in backend, frontend, DevOps, and production systems.

When a user provides an error message, follow this structure:

------------------------------------------------------------

## 1. Error Summary
- Briefly explain what this error means.
- Identify the type of error (syntax, runtime, dependency, configuration, etc.)

------------------------------------------------------------

## 2. Root Cause Analysis
- Clearly explain the most likely root cause.
- Mention possible alternative causes if relevant.

------------------------------------------------------------

## 3. Step-by-Step Fix
- Provide clear steps to resolve the issue.
- Include installation commands if required.
- Mention environment or version considerations.

------------------------------------------------------------

## 4. Corrected Code (If Applicable)
- Provide corrected version of the problematic code.
- Keep it clean and production-ready.

------------------------------------------------------------

## 5. Prevention Tips
- Briefly suggest how to avoid this issue in the future.

Be precise and practical.
Avoid unnecessary theory.
Focus on solving the problem efficiently.
1. Identify root cause
2. Provide fix
3. Provide corrected code
Structure the response clearly.

Given an error:
1. Identify root cause
2. Provide fix
3. Provide corrected code
Structure clearly.
"""


async def handle_advanced_debug(message: str):

    loop = asyncio.get_event_loop()

    async def safe_call(model_name):
        try:
            return await loop.run_in_executor(
                None,
                ask_openrouter,
                model_name,
                SYSTEM_PROMPT,
                message
            )
        except Exception as e:
            print(f"Model {model_name} failed:", str(e))
            return None

    # Run both safely in parallel
    task1 = safe_call(DEBUG_MODEL_1)
    task2 = safe_call(DEBUG_MODEL_2)

    response_1, response_2 = await asyncio.gather(task1, task2)

    # Decision logic
    if response_1 and response_2:
        return merge_debug_responses(response_1, response_2)

    elif response_1:
        return f"""
# ⚠ Partial Analysis (Model 1 Only)

{response_1}

Note: Second model was unavailable.
"""

    elif response_2:
        return f"""
# ⚠ Partial Analysis (Model 2 Only)

{response_2}

Note: First model was unavailable.
"""

    else:
        return """
# ❌ Debugging Service Temporarily Unavailable

Both AI models failed to respond.
Please try again in a few moments.
"""