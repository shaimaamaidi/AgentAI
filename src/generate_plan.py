def stream_structure(llm, structure):
    prompt = f"""
    Tu es un expert en organisation de projet pour tests unitaires.

    Voici la structure actuelle du projet :

    {structure}

    Indique comment organiser les fichiers uniquement de tests unitaires pour ce projet.
    Retourne uniquement la **nouvelle structure du dossier 'tests'**.
    """

    # Streaming de la réponse
    for chunk in llm.stream(prompt):
        if chunk.content:
            yield chunk.content
