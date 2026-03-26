#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генерация итогового Summary с подсчётом тестов
"""

import os
from pathlib import Path

def read_file(file_path, default="0"):
    try:
        return Path(file_path).read_text().strip() or default
    except:
        return default

def main():
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    
    # Считываем баллы
    structure = int(read_file("tools/output/structure_score.txt", "0"))
    lint = int(read_file("tools/output/lint_score.txt", "0"))
    lint_errors = int(read_file("tools/output/lint_error_count.txt", "0"))
    
    user_score = int(read_file("tools/output/user_score.txt", "0"))
    user_passed = int(read_file("tools/output/user_passed.txt", "0"))
    user_total = int(read_file("tools/output/user_total.txt", "0"))
    
    pet_score = int(read_file("tools/output/pet_score.txt", "0"))
    pet_passed = int(read_file("tools/output/pet_passed.txt", "0"))
    pet_total = int(read_file("tools/output/pet_total.txt", "0"))
    
    store_score = int(read_file("tools/output/store_score.txt", "0"))
    store_passed = int(read_file("tools/output/store_passed.txt", "0"))
    store_total = int(read_file("tools/output/store_total.txt", "0"))
    
    validation_score = int(read_file("tools/output/validation_score.txt", "0"))
    validation_passed = int(read_file("tools/output/validation_passed.txt", "0"))
    validation_total = int(read_file("tools/output/validation_total.txt", "0"))
    
    e2e_score = int(read_file("tools/output/e2e_score.txt", "0"))
    e2e_passed = int(read_file("tools/output/e2e_passed.txt", "0"))
    e2e_total = int(read_file("tools/output/e2e_total.txt", "0"))
    
    # Итого
    total_tests_passed = user_passed + pet_passed + store_passed + validation_passed + e2e_passed
    total_tests = user_total + pet_total + store_total + validation_total + e2e_total
    total_score = structure + lint + user_score + pet_score + store_score + validation_score + e2e_score
    max_score = 100
    percentage = (total_score * 100) // max_score if max_score > 0 else 0
    
    # Оценка
    if total_score >= 90:
        grade = "🟢 Отлично"
        status = "Зачтено"
    elif total_score >= 70:
        grade = "🟡 Хорошо"
        status = "Зачтено"
    elif total_score >= 50:
        grade = "🟠 Удовлетворительно"
        status = "Зачтено"
    else:
        grade = "🔴 Требуется доработка"
        status = "Не зачтено"
    
    # Прогресс-бар
    filled = percentage // 5
    empty = 20 - filled
    progress = "🟩" * filled + "⬜" * empty
    
    with open(summary_path, "a", encoding="utf-8") as s:
        s.write("\n---\n\n")
        s.write("# 🏆 ИТОГОВАЯ ОЦЕНКА\n\n")
        
        s.write("| Параметр | Значение |\n")
        s.write("|----------|----------|\n")
        s.write(f"| 💯 Баллы | **{total_score} / {max_score}** |\n")
        s.write(f"| 📈 Процент | **{percentage}%** |\n")
        s.write(f"| 🎓 Оценка | **{grade}** |\n")
        s.write(f"| ✅ Статус | **{status}** |\n")
        s.write(f"| 🧪 Тестов пройдено | **{total_tests_passed} / {total_tests}** |\n")
        s.write("\n")
        
        s.write("## Прогресс\n\n")
        s.write(f"`[{progress}]` {percentage}%\n\n")
        
        s.write("## 📋 Детализация по категориям\n\n")
        s.write("| Категория | Тесты | Баллы | Статус |\n")
        s.write("|-----------|-------|-------|--------|\n")
        
        s1 = "✅" if structure == 10 else "❌"
        s2 = "✅" if lint >= 12 else "⚠️"
        s3 = "✅" if user_passed >= 8 else "⚠️"
        s4 = "✅" if pet_passed >= 8 else "⚠️"
        s5 = "✅" if store_passed >= 5 else "⚠️"
        s6 = "✅" if validation_passed >= 5 else "⚠️"
        s7 = "✅" if e2e_passed >= 4 else "❌"
        
        s.write(f"| 📁 Структура | — | {structure} / 10 | {s1} |\n")
        s.write(f"| 🧹 Линтинг | {lint_errors} ошибок | {lint} / 15 | {s2} |\n")
        s.write(f"| 👤 User API | {user_passed} / {user_total} | {user_score} / 15 | {s3} |\n")
        s.write(f"| 🐾 Pet API | {pet_passed} / {pet_total} | {pet_score} / 20 | {s4} |\n")
        s.write(f"| 🛒 Store API | {store_passed} / {store_total} | {store_score} / 15 | {s5} |\n")
        s.write(f"| ✅ Validation | {validation_passed} / {validation_total} | {validation_score} / 15 | {s6} |\n")
        s.write(f"| 🔄 E2E Tests | {e2e_passed} / {e2e_total} | {e2e_score} / 25 | {s7} |\n")
        s.write("\n")
        
        s.write("## 📎 Артефакты\n\n")
        s.write("Все артефакты доступны в разделе **Actions → Artifacts**.\n\n")
        
        s.write("| Тип | Путь |\n")
        s.write("|-----|------|\n")
        s.write("| 📸 Allure-отчёт | `allure-results/` |\n")
        s.write("| 📄 Логи | `logs/` |\n")
        s.write("| 📊 JSON результаты | `tools/output/` |\n")
        s.write("| 🧹 Линтинг отчёт | `tools/output/flake8_report.txt` |\n")
        s.write("\n")
        
        s.write("---\n\n")
        s.write(f"**💪 ИТОГО: {total_score} баллов из {max_score}**\n\n")
        s.write(f"**🧪 Тестов: {total_tests_passed} / {total_tests}**\n\n")
        s.write("*GitHub Classroom Autograder • 2026.03*\n")

if __name__ == "__main__":
    main()