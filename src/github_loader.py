import subprocess
import os
import shutil


def is_git_url_valid(repo_url: str) -> bool:
    try:
        result = subprocess.run(
            ["git", "ls-remote", repo_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
        return result.returncode == 0
    except subprocess.SubprocessError:
        return False

def clone_repo(repo_url):
    if not os.path.exists("repo"):
        subprocess.run(["git", "clone", repo_url, "repo"])

def delete_repo():
    """Supprime le dossier 'repo' et tout son contenu, même sur Windows."""

    def remove_readonly(func, path, excinfo):
        import stat, os
        os.chmod(path, stat.S_IWRITE)
        func(path)

    if os.path.exists("repo"):
        shutil.rmtree("repo", onerror=remove_readonly)
