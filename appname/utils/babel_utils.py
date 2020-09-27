from flask import request, g


def get_locale():
    try:
        rv = request.accept_languages.best_match(["zh", "en", "es", "de", "ko"])
        return rv
    except RuntimeError:  # Working outside of request context.
        return g.get('local')
