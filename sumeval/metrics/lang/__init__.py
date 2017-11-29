def get_lang(lang=""):
    if lang == "ja":
        from .lang_ja import LangJA
        return LangJA()
    else:
        from .lang_en import LangEN
        return LangEN()
