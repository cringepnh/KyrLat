# -*- coding: utf-8 -*-
"""
Uzbek Cyrillic ↔ Latin Transliteration Module

This module provides rule-based transliteration between Uzbek Cyrillic and Latin scripts.
No AI or machine learning - purely deterministic character mapping.
"""

# =============================================================================
# TEXT NORMALIZATION
# =============================================================================

def normalize_apostrophes(text: str) -> str:
    """
    Normalize all apostrophe-like characters to the standard Uzbek apostrophe (U+02BB).
    
    This MUST be called before any transliteration logic.
    
    Converts:
    - ' (U+0027, ASCII apostrophe)
    - ` (U+0060, grave accent)
    - ʼ (U+02BC, modifier letter apostrophe)
    - ' (U+2019, right single quotation mark)
    
    To:
    - ʻ (U+02BB, modifier letter turned comma - Uzbek standard)
    """
    UZBEK_APOSTROPHE = '\u02BB'  # ʻ
    
    apostrophe_variants = [
        '\u0027',  # ' ASCII apostrophe
        '\u0060',  # ` grave accent
        '\u02BC',  # ʼ modifier letter apostrophe
        '\u2019',  # ' right single quotation mark
    ]
    
    for variant in apostrophe_variants:
        text = text.replace(variant, UZBEK_APOSTROPHE)
    
    return text


# =============================================================================
# MAPPING TABLES
# Official Uzbek Cyrillic ↔ Latin (1995 standard)
# =============================================================================

# IMPORTANT: Uzbek Cyrillic alphabet does NOT include Ң (eng)!
# The sound "ng" is written as two letters: Н + Г (нг) in Cyrillic

# Latin → Cyrillic: Multi-character combinations (MUST be processed FIRST)
LATIN_TO_CYRILLIC_MULTI = [
    # Uppercase combinations with apostrophe
    ("G\u02BB", "Ғ"),   # Gʻ → Ғ
    ("O\u02BB", "Ў"),   # Oʻ → Ў
    # Apostrophe as digraph separator (MUST come BEFORE sh/ch!)
    # These prevent s'h → ш, instead s'h → сҳ (Is'hoq → Исҳоқ)
    ("S\u02BBh", "Сҳ"), # S'h → Сҳ (not Ш)
    ("s\u02BBh", "сҳ"), # s'h → сҳ (not ш)
    ("S\u02BBH", "СҲ"), # S'H → СҲ
    ("C\u02BBh", "Чҳ"), # C'h → Чҳ (not Ч) if needed
    ("c\u02BBh", "чҳ"), # c'h → чҳ (not ч) if needed
    # Uppercase digraphs
    ("Sh", "Ш"),
    ("Ch", "Ч"),
    ("Ng", "Нг"),  # ng → нг (two separate Cyrillic letters, NOT ң!)
    ("Yo", "Ё"),
    ("Yu", "Ю"),
    ("Ya", "Я"),
    # Lowercase combinations with apostrophe
    ("g\u02BB", "ғ"),   # gʻ → ғ
    ("o\u02BB", "ў"),   # oʻ → ў
    # Lowercase digraphs
    ("sh", "ш"),
    ("ch", "ч"),
    ("ng", "нг"),  # ng → нг (two separate Cyrillic letters, NOT ң!)
    ("yo", "ё"),
    ("yu", "ю"),
    ("ya", "я"),
    # All uppercase variants
    ("SH", "Ш"),
    ("CH", "Ч"),
    ("NG", "НГ"),  # NG → НГ
    ("YO", "Ё"),
    ("YU", "Ю"),
    ("YA", "Я"),
]

# Latin → Cyrillic: Single character mappings
LATIN_TO_CYRILLIC_SINGLE = {
    # Uppercase
    'A': 'А', 'B': 'Б', 'D': 'Д', 'E': 'Е', 'F': 'Ф',
    'G': 'Г', 'H': 'Ҳ', 'I': 'И', 'J': 'Ж', 'K': 'К',
    'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П',
    'Q': 'Қ', 'R': 'Р', 'S': 'С', 'T': 'Т', 'U': 'У',
    'V': 'В', 'X': 'Х', 'Y': 'Й', 'Z': 'З',
    # Lowercase
    'a': 'а', 'b': 'б', 'd': 'д', 'e': 'е', 'f': 'ф',
    'g': 'г', 'h': 'ҳ', 'i': 'и', 'j': 'ж', 'k': 'к',
    'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п',
    'q': 'қ', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у',
    'v': 'в', 'x': 'х', 'y': 'й', 'z': 'з',
    # Apostrophe → Hard sign (ъ) for words like ra'no → раъно, ma'no → маъно
    # Note: s'h is handled separately in MULTI to prevent → ш (becomes сҳ)
    '\u02BB': 'ъ',  # Tutuq belgisi → ъ (hard sign)
}

# Cyrillic → Latin mappings
# Official Uzbek Cyrillic alphabet: А Б В Г Д Е Ё Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Ъ Ь Э Ю Я Ў Қ Ғ Ҳ
CYRILLIC_TO_LATIN = {
    # Uppercase
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Ғ': "G\u02BB",  # Ғ → Gʻ
    'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'J', 'З': 'Z',
    'И': 'I', 'Й': 'Y', 'К': 'K', 'Қ': 'Q', 'Л': 'L',
    'М': 'M', 'Н': 'N', 'О': 'O', 'Ў': "O\u02BB",  # Ў → Oʻ
    'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
    'Ф': 'F', 'Х': 'X', 'Ҳ': 'H', 'Ч': 'Ch', 'Ш': 'Sh',
    'Ъ': "'", 'Ь': '', 'Э': 'E', 'Ц': 'Ts',  # Russian letters sometimes used
    'Ю': 'Yu', 'Я': 'Ya',
    # Lowercase
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'ғ': "g\u02BB",  # ғ → gʻ
    'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'j', 'з': 'z',
    'и': 'i', 'й': 'y', 'к': 'k', 'қ': 'q', 'л': 'l',
    'м': 'm', 'н': 'n', 'о': 'o', 'ў': "o\u02BB",  # ў → oʻ
    'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'x', 'ҳ': 'h', 'ч': 'ch', 'ш': 'sh',
    'ъ': "'", 'ь': '', 'э': 'e', 'ц': 'ts',  # Russian letters sometimes used
    'ю': 'yu', 'я': 'ya',
}


# =============================================================================
# TRANSLITERATION FUNCTIONS
# =============================================================================

def latin_to_cyrillic(text: str) -> str:
    """
    Transliterate Latin text to Cyrillic.
    
    Process order:
    1. Normalize apostrophes
    2. Replace multi-character combinations FIRST
    3. Replace single characters
    
    Numbers, spaces, and punctuation remain unchanged.
    """
    # Step 0: Normalize apostrophes
    text = normalize_apostrophes(text)
    
    # Step 1: Process multi-character combinations FIRST (order matters!)
    for latin, cyrillic in LATIN_TO_CYRILLIC_MULTI:
        text = text.replace(latin, cyrillic)
    
    # Step 2: Process single characters
    result = []
    for char in text:
        if char in LATIN_TO_CYRILLIC_SINGLE:
            result.append(LATIN_TO_CYRILLIC_SINGLE[char])
        else:
            # Keep numbers, spaces, punctuation unchanged
            result.append(char)
    
    return ''.join(result)


def cyrillic_to_latin(text: str) -> str:
    """
    Transliterate Cyrillic text to Latin.
    
    Output uses ʻ (U+02BB) as the standard Uzbek apostrophe.
    Numbers, spaces, and punctuation remain unchanged.
    """
    result = []
    for char in text:
        if char in CYRILLIC_TO_LATIN:
            result.append(CYRILLIC_TO_LATIN[char])
        else:
            # Keep numbers, spaces, punctuation unchanged
            result.append(char)
    
    return ''.join(result)


def transliterate(text: str, direction: str) -> str:
    """
    Main transliteration function.
    
    Args:
        text: Input text to transliterate
        direction: Either "lat_to_cyr" or "cyr_to_lat"
    
    Returns:
        Transliterated text
    """
    if direction == "lat_to_cyr":
        return latin_to_cyrillic(text)
    elif direction == "cyr_to_lat":
        return cyrillic_to_latin(text)
    else:
        raise ValueError(f"Unknown direction: {direction}. Use 'lat_to_cyr' or 'cyr_to_lat'")


# =============================================================================
# TESTING (only runs if executed directly)
# =============================================================================

if __name__ == "__main__":
    # Test cases
    test_latin = "O'zbekiston Respublikasi"
    test_cyrillic = "Ўзбекистон Республикаси"
    
    print("=== Transliteration Test ===\n")
    
    # Test Latin → Cyrillic
    result1 = transliterate(test_latin, "lat_to_cyr")
    print(f"Latin → Cyrillic:")
    print(f"  Input:  {test_latin}")
    print(f"  Output: {result1}")
    print()
    
    # Test Cyrillic → Latin
    result2 = transliterate(test_cyrillic, "cyr_to_lat")
    print(f"Cyrillic → Latin:")
    print(f"  Input:  {test_cyrillic}")
    print(f"  Output: {result2}")
