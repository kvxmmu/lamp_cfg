from importlib import import_module


def import_hook(package):
    top_pos = package.rfind('.')
    top_package = package[:top_pos]
    classname = package[top_pos+1:]

    return getattr(import_module(top_package), classname)
