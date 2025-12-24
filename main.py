from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from src.github_loader import clone_repo, delete_repo, is_git_url_valid
from src.generate_tests_by_file import generate_tests_by_file
from src.generate_plan import stream_structure
from src.project_structure import get_project_structure
from src.structure_cleaner import clean_structure

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_index():
    return FileResponse("static/index.html")


@app.get("/health")
async def health_check():
    return {"message": "API is healthy"}


@app.get("/generate-tests")
def generate_tests_endpoint(url_repo):
    if not is_git_url_valid(url_repo):
        raise HTTPException(status_code=400, detail="URL Git invalide")

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY manquante")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        streaming=True,
        api_key=api_key
    )

    try:
        clone_repo(url_repo)

        structure = get_project_structure()
        structure_cleaned = clean_structure(structure)

        project_plan = stream_structure(llm, structure_cleaned)

        ai_response = {}
        generate_tests_by_file(llm, ai_response)

        # Streaming
        def generator():
            yield "Structure du projet\n\n"

            for chunk in project_plan:
                yield chunk

            yield "\n\n"

            for file in ai_response.get("files", []):
                yield f"\n\n### Tests pour {file['path']}\n\n"
                for chunk in file["code"]:
                    yield chunk
        return StreamingResponse(generator(), media_type="text/plain")

    finally:
        delete_repo()
