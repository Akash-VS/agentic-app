import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)


# 🔹 Text Generation
def ask_gpt(system_prompt: str, user_message: str):

    full_prompt = f"""
{system_prompt}

User Input:
{user_message}
"""

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)

        response = model.generate_content(full_prompt)

        return response.text if response and response.text else "No response generated."

    except Exception as e:
        print("Gemini error:", str(e))
        return "Gemini failed to generate response."


# 🔹 OCR / Screenshot Text Extraction
def extract_text_with_gemini(image_bytes: bytes):

    try:
        model = genai.GenerativeModel(GEMINI_MODEL)

        response = model.generate_content(
            [
                "Extract all visible programming error text from this image clearly.",
                {"mime_type": "image/png", "data": image_bytes},
            ]
        )

        return response.text if response and response.text else "No readable text found."

    except Exception as e:
        print("Gemini OCR error:", str(e))
        return "Failed to extract text from image."
