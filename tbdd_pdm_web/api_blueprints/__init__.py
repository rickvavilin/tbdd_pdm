__author__ = 'Aleksandr Vavilin'
from pkgutil import iter_modules
from flask import Blueprint


def register_api_blueprints(app):
    _blueprints = _get_blueprints()
    for node, bpmodule, blueprint in _blueprints:
        app.logger.info("Registring API blueprint %s" % node)
        app.register_blueprint(blueprint, url_prefix='/api/' + blueprint.name)


def _get_blueprints():
    """docstring for _get_blueprints"""
    _blueprints = []

    for _loader, name, _ispkg in iter_modules(path=__path__):
        fullnamespace = ".".join([__name__, name])
        blueprint_module = __import__(fullnamespace, fromlist=".")
        blueprint_class = getattr(blueprint_module, 'node', None)
        if blueprint_class and blueprint_class.__class__ == Blueprint:
            _blueprints.append((name, blueprint_module, blueprint_class))

    return _blueprints