import os
import requests
import sys
import re

# Try to get API key from Anki addon config first, then fall back to environment variable
try:
    from aqt import mw

    if mw and mw.addonManager:
        config = mw.addonManager.getConfig(__name__)
        API_KEY = config.get("esv_api_key") if config else None
    else:
        API_KEY = None

except ImportError:
    # Running outside of Anki (e.g., for testing)
    import dotenv

    dotenv.load_dotenv()
    API_KEY = os.getenv("ESV_API_KEY")

API_URL = "https://api.esv.org/v3/passage/text/"


def clean_bible_text(text):
    """Format Bible text preserving HTML tags and adding proper line breaks."""
    if not text:
        return text

    # Clean up extra whitespace but preserve HTML
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    # Convert [number] format to <sup>number</sup> format
    text = re.sub(r"\[(\d+)\]", r"<sup>\1</sup>", text)

    # Split by verse numbers and add line breaks
    parts = re.split(r"(<sup>\d+</sup>)", text)

    formatted_verses = []
    current_verse = ""

    for i, part in enumerate(parts):
        if re.match(r"<sup>\d+</sup>", part):
            # This is a verse number
            if current_verse.strip():
                formatted_verses.append(current_verse.strip())
            current_verse = part
        else:
            # This is verse text
            current_verse += part

    # Add the last verse
    if current_verse.strip():
        formatted_verses.append(current_verse.strip())

    # Join verses with line breaks
    formatted_text = "\n".join(v for v in formatted_verses if v.strip())

    return formatted_text


def get_esv_text(passage):
    params = {
        "q": passage,
        "include-headings": False,
        "include-footnotes": False,
        "include-verse-numbers": True,  # Changed to True to get verse numbers
        "include-short-copyright": False,
        "include-passage-references": False,
    }

    headers = {"Authorization": "Token %s" % API_KEY}

    response = requests.get(API_URL, params=params, headers=headers)

    passages = response.json()["passages"]
    raw_text = passages[0].strip() if passages else "Error: Passage not found"

    # Clean and format the text
    return clean_bible_text(raw_text)


if __name__ == "__main__":
    passage = " ".join(sys.argv[1:])

    if passage:
        print(get_esv_text(passage))
