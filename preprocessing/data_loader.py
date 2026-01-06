from typing import List, Dict

class DataLoader:
    def __init__(self):
        # In a real scenario, paths to dataset files would be passed here
        pass

    def load_codesearchnet_sample(self):
        """
        Returns a dummy sample mimicking CodeSearchNet structure.
        """
        return [
            {
                "func_name": "sort_list",
                "code": "def sort_list(l): return sorted(l)",
                "docstring": "Sorts a list in ascending order.",
                "language": "python"
            },
            {
                "func_name": "dummy_buggy",
                "code": "def divide(a, b): return a / 0",
                "docstring": "Intentionally buggy division.",
                "language": "python"
            }
        ]

    def load_sard_sample(self):
        """
        Returns a dummy sample mimicking SARD vulnerability dataset.
        """
        return [
            {
                "id": "SARD-101",
                "code": "char buffer[10]; strcpy(buffer, large_input);",
                "vulnerability": "Buffer Overflow",
                "language": "c"
            }
        ]
