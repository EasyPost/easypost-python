# Imports needed in setup.py and __init__.py

def import_json():
    # Python 2.5 and below do not ship with json
    _json_loaded = None
    try:
        import json
        if hasattr(json, 'loads'):
            return json
        _json_loaded = False
    except ImportError:
        pass

    try:
        import simplejson
        return simplejson
    except ImportError:
        raise ImportError("EasyPost requires a JSON library. Please try installing the python simplejson library via 'pip install simplejson' or 'easy_install simplejson', or contact us at contact@easypost.com.")
