def get_preference_from_persona(persona):
    """
    Map user persona to preference
    """

    if persona == "student":
        return "cheap"

    elif persona == "business":
        return "fast"

    elif persona == "tourist":
        return "comfortable"

    elif persona == "eco":
        return "balanced"

    else:
        return "cheap"