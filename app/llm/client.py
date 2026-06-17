import os
from dotenv import load_dotenv
from groq import Groq
import time

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

import time

def call_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"LLM Error: {e}")
        time.sleep(3)

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"LLM Error: {str(e)}"