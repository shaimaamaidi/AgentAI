def stream_test(llm, code):
    prompt = f"""
    Tu es un expert en tests unitaires.
    
    Génère des tests unitaires pour le code ci-dessous en utilisant pytest.
    Retourne uniquement le **code des tests**, suivi d'une petite explication de 1 à 2 phrases à la fin.
    Ne rajoute pas de texte inutile avant ou après le code.
    
    CODE :
    {code}
    """
    for chunk in llm.stream(prompt):
        if chunk.content:
            yield chunk.content


