"""Opt-in loading of third-party recognizer methods."""

from collections.abc import Callable, Iterable
from inspect import isfunction

import pluggy

from . import Recognizer

_PROJECT_NAME = "speech_recognition"
_hookspec = pluggy.HookspecMarker(_PROJECT_NAME)
hookimpl = pluggy.HookimplMarker(_PROJECT_NAME)


class _RecognizerHooks:
    @_hookspec
    def recognizer_methods(self) -> Iterable[tuple[str, Callable[..., object]]]:
        """Return (name, function) pairs for methods taking (self, audio_data, ...)."""


def load_recognizer_plugins() -> None:
    """Load installed speech_recognition entry points and extend Recognizer.

    Call once at startup, and only with trusted plugins installed. Plugins
    cannot replace existing recognizer methods or claim the same method name.
    """
    manager = pluggy.PluginManager(_PROJECT_NAME)
    manager.add_hookspecs(_RecognizerHooks)
    manager.load_setuptools_entrypoints(_PROJECT_NAME)
    manager.check_pending()

    methods = {}
    for plugin_methods in manager.hook.recognizer_methods():
        for name, function in plugin_methods:
            if not name.startswith("recognize_") or name == "recognize_" or not name.isidentifier():
                raise ValueError(f"Invalid recognizer method name: {name!r}")
            if not isfunction(function):
                raise TypeError(f"{name!r} must be a function taking (self, audio_data, ...)")
            if name in methods or hasattr(Recognizer, name):
                raise ValueError(f"Recognizer method {name!r} already exists")
            methods[name] = function

    for name, function in methods.items():
        setattr(Recognizer, name, function)
