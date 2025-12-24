from pathlib import Path

def get_project_structure(base_dir="repo"):
    """
    Retourne une représentation simple de la structure du projet.
    Exemple :
    repo/
        src/
            main.py
        tests/
    """
    structure = "Structure du projet :\n"
    for path in Path(base_dir).rglob("*"):
        depth = len(path.relative_to(base_dir).parts)
        prefix = "    " * depth
        if path.is_dir():
            structure += f"{prefix}{path.name}/\n"
        else:
            structure += f"{prefix}{path.name}\n"
    return structure
