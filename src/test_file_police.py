from pathlib import Path

# Mots-clés parasites / non métiers
FORBIDDEN_KEYWORDS = {
    "example",
    "exemple",
    "sample",
    "dummy",
    "mock",
    "fixture",
}

# Fichiers jamais testés directement
FORBIDDEN_FILES = {
    "__init__.py",

    # Python
    "setup.py",
    "requirements.txt",

    # JS / TS
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",

    # Angular / React / Tooling
    "angular.json",
    "vite.config.ts",
    "vite.config.js",
    "webpack.config.js",
    "tsconfig.json",
    "tsconfig.app.json",
    "tsconfig.spec.json",

    # Spring Boot
    "pom.xml",
    "build.gradle",
    "settings.gradle",
}

# Extensions non exécutables ou non testables
FORBIDDEN_EXTENSIONS = {
    ".md", ".txt", ".json", ".yml", ".yaml",
    ".xml", ".env", ".ini", ".properties",

    # Assets
    ".html", ".css", ".scss", ".less",
    ".svg", ".png", ".jpg", ".jpeg", ".gif"
}

# Dossiers à ignorer totalement
FORBIDDEN_DIRS = {
    ".git", ".idea", ".vscode",
    "__pycache__", ".venv", "venv",

    # JS
    "node_modules",

    # Build
    "dist", "build", "target", "out",

    # Angular
    ".angular", ".nx",

    "tests",
    "docs"
}

# Fichiers déjà des tests
TEST_FILE_PATTERNS = (
    ".spec.", ".test."
)

FORBIDDEN_FILES |= {
    "main.py",
    "conf.py",
    "__main__.py",
}

# Langages supportés
SUPPORTED_EXTENSIONS = {
    ".py", ".java",
    ".js", ".jsx",
    ".ts", ".tsx",
    ".c", ".cpp"
}


def should_generate_tests(file: Path) -> bool:
    if not file.is_file():
        return False

    file_name = file.name.lower()
    suffix = file.suffix.lower()

    # 1️⃣ Dossiers interdits
    if any(part in FORBIDDEN_DIRS for part in file.parts):
        return False

    # 2️⃣ Fichiers explicitement exclus
    if file_name in FORBIDDEN_FILES:
        return False

    # 3️⃣ Extensions interdites
    if suffix in FORBIDDEN_EXTENSIONS:
        return False

    if suffix in FORBIDDEN_FILES:
        return False

    # 4️⃣ Déjà un fichier de test
    if any(p in file_name for p in TEST_FILE_PATTERNS):
        return False

    # 5️⃣ Mots-clés parasites
    if any(k in file_name for k in FORBIDDEN_KEYWORDS):
        return False

    # 6️⃣ Langage supporté
    if suffix not in SUPPORTED_EXTENSIONS:
        return False

    return True
