import re

# Mots-clés parasites (LLM, commentaires, exemples)
FORBIDDEN_KEYWORDS = {
    "example",
    "exemple",
    "sample",
    "dummy",
    "placeholder",
}

# Fichiers jamais nécessaires dans une structure de tests
FORBIDDEN_FILES = {
    "__init__.py",
    "index.ts",
    "index.js",
    "main.ts",
    "main.js",
    "polyfills.ts",
    "environment.ts",
    "setup.py",
    "requirements.txt",
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pom.xml",
    "build.gradle",
    "settings.gradle",
}

# Extensions non pertinentes pour décrire des tests
FORBIDDEN_EXTENSIONS = {
    ".md",
    ".txt",
    ".json",
    ".yml",
    ".yaml",
    ".xml",
    ".env",
    ".properties",
    ".html",
    ".css",
    ".scss",
}

# Dossiers à ignorer
FORBIDDEN_DIRS = {
    "node_modules",
    ".git",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "target",
    ".angular",
}

# Regex pour commentaires (tous langages)
COMMENT_PATTERNS = [
    r"#.*$",        # Python / Shell
    r"//.*$",       # JS / Java
    r"/\*.*\*/",    # Commentaires bloc
]


def clean_structure(structure_text: str) -> str:
    cleaned_lines = []

    for line in structure_text.splitlines():
        raw = line.strip().lower()

        if not raw:
            continue

        if any(re.search(pattern, raw) for pattern in COMMENT_PATTERNS):
            continue

        if any(word in raw for word in FORBIDDEN_KEYWORDS):
            continue

        if any(raw.endswith(f) for f in FORBIDDEN_FILES):
            continue

        if any(raw.endswith(ext) for ext in FORBIDDEN_EXTENSIONS):
            continue

        if any(f"/{d}/" in raw or raw == f"{d}/" for d in FORBIDDEN_DIRS):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)
