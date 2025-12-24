from pathlib import Path
from src.generate_unit_tests import stream_test
from src.test_file_police import should_generate_tests


def generate_tests_by_file(llm, ai_response: dict):
    ai_response.setdefault("files", [])

    for file in Path("repo").rglob("*"):
        if not file.is_file():
            continue

        if not should_generate_tests(file):
            continue

        try:
            code = file.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"[WARN] Impossible de lire le fichier {file}: {e}")
            continue

        
        ai_response["files"].append({
            "path": file.as_posix(),
            "code": stream_test(llm, code)
        })
