"""https://mymemory.translated.net/doc/spec.php"""

import requests

URL = "https://api.mymemory.translated.net/get"

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    params = {
        "q": text,
        "langpair": f"{source_lang}|{target_lang}",
        "de": "rubenvandamme88@gmail.com" # using a valid email, you can translate up to 50000 characters a day
    }
    
    response = requests.get(URL, params=params)
    
    # check for HTTP errors
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.reason}")
    
    data = response.json()
    
    # check if the API response contains an error
    if "responseStatus" in data and data["responseStatus"] != 200:
        error_message = data.get("responseDetails", "Unknown error")
        raise Exception(f"MyMemory API error: {error_message}")
    
    return data["responseData"]["translatedText"]
