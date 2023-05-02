from config import Config


def is_extension_allowed(filename):
    return filename.split('.')[-1] in Config.ALLOWED_EXTENSIONS
