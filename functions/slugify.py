import re


eng_letters = {char: char for char in "abcdefghijklmnopqrstuvwxyz"}
ru_letters = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}
digits = {char: char for char in "0123456789"}
symbols = {"-": "-", "$": "dollar", "&": "and"}

alphabet = eng_letters | ru_letters | digits | symbols

def slugify(string: str): 
    # string into stripped lowercase string
    string = string.lower().strip()
    
    # converting multiple spaces and dashes into one dash 
    string = re.sub(r"[ -]+", "-", string)
    
    # alphabet modification
    slug = ""
    for char in string:
        slug += alphabet.get(char, "")

    # converting multiple spaces and dashes into one dash 
    slug = re.sub(r"[ -]+", "-", slug)
        
    return slug