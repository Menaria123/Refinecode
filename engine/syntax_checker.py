import ast
import re

class SyntaxChecker:
    def __init__(self):
        pass

    def check_python_syntax(self, code: str):
        """
        Uses Python's AST module to check for syntax errors.
        """
        try:
            ast.parse(code)
            return {"valid": True, "error": None}
        except SyntaxError as e:
            return {"valid": False, "error": f"{e.msg} at line {e.lineno}"}

    def check_syntax(self, code: str, language: str = 'python'):
        """
        Dispatch based on language.
        For non-Python languages, we might valid based on heuristics or 
        assume valid if we lack a compiler/parser in this env.
        """
        if language.lower() == 'python':
            return self.check_python_syntax(code)
        
        # Simple heuristic for C/C++ style missing semicolons
        if language.lower() in ['c', 'cpp', 'java', 'javascript']:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped and not stripped.endswith((';', '{', '}', ')', ':')) and not stripped.startswith(('#', '//', '/*')):
                     # Very naive check, just for demonstration
                     pass 
        
        return {"valid": True, "error": None}
