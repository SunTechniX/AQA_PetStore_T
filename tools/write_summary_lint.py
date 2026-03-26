#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/write_summary_lint.py
Вывод отчёта flake8 в GitHub Step Summary
"""

import os
from pathlib import Path

def main():
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    
    report_path = Path("tools/output/flake8_report.txt")
    score_path = Path("tools/output/lint_score.txt")
    error_count_path = Path("tools/output/lint_error_count.txt")
    
    error_count = 0
    score = 0
    
    if error_count_path.exists():
        error_count = int(error_count_path.read_text().strip() or "0")
    
    if score_path.exists():
        score = int(score_path.read_text().strip() or "0")
    
    with open(summary_path, "a", encoding="utf-8") as s:
        s.write("\n## 🧹 Линтинг (flake8)\n\n")
        
        if error_count == 0:
            s.write("✅ **Ошибок не найдено!** Код соответствует стандартам.\n\n")
        else:
            s.write(f"⚠️ **Найдено ошибок:** `{error_count}`\n\n")
            
            if report_path.exists():
                content = report_path.read_text(encoding="utf-8")
                # Показываем первые 10 ошибок
                lines = [l for l in content.split('\n') if l.strip() and ':' in l][:10]
                if lines:
                    s.write("### Примеры ошибок для исправления:\n\n```")
                    s.write('\n'.join(lines))
                    s.write("\n```\n\n")
            
            s.write("💡 **Совет:** Исправьте ошибки по порядку. Запустите локально:\n")
            s.write("```bash\n")
            s.write("flake8 . --config=tools/flake8_config.cfg --show-source\n")
            s.write("```\n\n")
        
        s.write(f"**Баллы:** `{score} / 15`\n\n")

if __name__ == "__main__":
    main()