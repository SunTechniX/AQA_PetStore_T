#!/usr/bin/env python3
"""
Проверка структуры проекта
"""

import sys
from pathlib import Path

def main():
    required = {
        "api_client/": False,
        "tests/": False,
        "schemas/": False,
        "conftest.py": False,
        "pytest.ini": False,
        "requirements.txt": False
    }
    
    for path in required.keys():
        required[path] = Path(path).exists()
    
    all_exist = all(required.values())
    print("PASS" if all_exist else "FAIL")
    sys.exit(0)

if __name__ == "__main__":
    main()