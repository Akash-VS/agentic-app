from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL

# Create client
client = genai.Client(api_key=GEMINI_API_KEY)


# 🔹 Text Generation
def ask_gpt(system_prompt: str, user_message: str):

    full_prompt = f"""
{system_prompt}

User Input:
{user_message}
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=full_prompt
        )

        return response.text if response and response.text else "No response generated."

    except Exception as e:
        print("Gemini error:", str(e))
        return "Gemini failed to generate response."



from google.genai import types

def extract_text_with_gemini(image_bytes: bytes):

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                "Extract all visible programming error text from this image clearly.",
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/png"
                )
            ]
        )

        return response.text if response and response.text else "No readable text found."

    except Exception as e:
        print("Gemini OCR error:", str(e))
        return "Failed to extract text from image."

# You can add more Gemini-related functions here as needed.