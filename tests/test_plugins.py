from unittest.mock import patch

import pytest

import speech_recognition as sr
from speech_recognition import plugins


def recognize_test(self, audio_data, *, label):
    return self.energy_threshold, audio_data, label


@pytest.fixture
def recognizer_class(monkeypatch):
    class TestRecognizer(sr.Recognizer):
        pass

    monkeypatch.setattr(plugins, "Recognizer", TestRecognizer)
    return TestRecognizer


def load_test_plugin(methods):
    class Plugin:
        @plugins.hookimpl
        def recognizer_methods(self):
            return methods

    def discover(manager, group):
        assert group == "speech_recognition"
        manager.register(Plugin())
        return 1

    with patch.object(plugins.pluggy.PluginManager, "load_setuptools_entrypoints", discover):
        plugins.load_recognizer_plugins()


def test_load_recognizer_plugins_binds_method_to_existing_instance(recognizer_class):
    recognizer = recognizer_class()
    audio = sr.AudioData(b"\x00\x00", 16000, 2)

    assert not hasattr(recognizer, "recognize_test")
    load_test_plugin([("recognize_test", recognize_test)])

    assert recognizer.recognize_test(audio, label="test") == (300, audio, "test")


@pytest.mark.parametrize("name", ["recognize_test", "recognize_api"])
def test_load_recognizer_plugins_rejects_conflicts_without_adding_methods(recognizer_class, name):
    with pytest.raises(ValueError, match=f"Recognizer method '{name}' already exists"):
        load_test_plugin([("recognize_test", recognize_test), (name, recognize_test)])

    assert not hasattr(recognizer_class, "recognize_test")
