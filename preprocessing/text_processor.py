import nltk
from nltk.tokenize import word_tokenize
import re

# Download necessary NLTK data (safe to run multiple times)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class TextProcessor:
    def __init__(self):
        pass

    def tokenize_code(self, code_snippet: str):
        """
        Simple tokenization for source code.
        Splits by non-alphanumeric characters but keeps them as tokens.
        """
        # Using regex to split but keep delimiters could be one way, 
        # but NLTK's word_tokenize is often decent for a first pass on comments/docs.
        # For strict code, we might want just whitespace or specific regex.
        # This is a hybrid approach.
        return word_tokenize(code_snippet)

    def normalize_text(self, text: str):
        """
        Lowercases and removes extra whitespace.
        """
        return " ".join(text.lower().split())

    def extract_comments(self, code: str, lang: str = 'python'):
        """
        Basic comment extraction (heuristic).
        """
        if lang == 'python':
            return re.findall(r'#.*', code)
        elif lang in ['java', 'cpp', 'javascript']:
            return re.findall(r'//.*', code)
        return []
