import openai
import os
from dotenv import load_dotenv
import time
from typing import List

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o"
API_DELAY = 1

def parse_with_gpt(dom_chunks: List[str], parse_description: str) -> str:
    """
    Parse chunks of DOM content using GPT to extract specific information based on a description.
    
    Args:
        dom_chunks (List[str]): List of DOM content chunks to parse.
        parse_description (str): Description of the information to extract.
    
    Returns:
        str: Concatenated parsed results separated by newlines.
    
    Raises:
        ValueError: If inputs are invalid.
        Exception: If API call fails.
    """
    # Input validation
    if not dom_chunks or not isinstance(dom_chunks, list):
        raise ValueError("dom_chunks must be a non-empty list")
    if not parse_description or not isinstance(parse_description, str):
        raise ValueError("parse_description must be a non-empty string")

    parsed_result = []

    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            PROMPT = (
                f"You are tasked with extracting specific information from the following text content: {chunk}. "
                "Please follow these instructions carefully: \n\n"
                "1. **Extract Information:** Only extract the information that directly matches the user-provided description. "
                "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
                "3. **Empty Response:** If no information matches the description, return an empty string (''). "
                "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
            )
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": PROMPT},
                    {"role": "user", "content": [{"type": "text", "text": parse_description}]},
                ],
                max_tokens=6000,
            )
            content = resp.choices[0].message.content.strip() if resp.choices[0].message.content else ""
            parsed_result.append(content)
            print(f"Log: parsed {i}/{len(dom_chunks)} batches")

            # Add delay to respect API rate limits
            time.sleep(API_DELAY)

        except openai.OpenAIError as e:
            print(f"Error parsing chunk {i}: {str(e)}")
            parsed_result.append("")  # Append empty string on error
        except Exception as e:
            print(f"Unexpected error parsing chunk {i}: {str(e)}")
            parsed_result.append("")  # Append empty string on error

    return "\n".join(parsed_result)