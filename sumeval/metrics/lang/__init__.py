def get_lang(lang=""):
    if lang == "ja":
        from .lang_ja import LangJA
        return LangJA()
    elif lang == "zh":
        from .lang_zh import LangZH
        return LangZH()
    else:
        from .lang_en import LangEN
        return LangEN()
