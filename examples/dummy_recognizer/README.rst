Third-party recognizer plugin prototype
=======================================

In a virtual environment, run this from the SpeechRecognition repository root:

.. code-block:: console

    python -m pip install -e ".[dev]" ./examples/dummy_recognizer

.. code-block:: python

    import speech_recognition as sr
    from speech_recognition.plugins import load_recognizer_plugins

    load_recognizer_plugins()
    r = sr.Recognizer()
    audio = sr.AudioData(b"\x00\x00", 16000, 2)
    print(r.recognize_dummy(audio))  # dummy transcript (16000 Hz)

The loader discovers installed entry points in the ``speech_recognition`` group.
Their modules implement the ``recognizer_methods`` hook with ``@hookimpl`` and
return pairs of a ``recognize_*`` name and a function taking
``(self, audio_data, ...)``. Once loaded, the methods are available on existing
and new ``Recognizer`` instances without changing built-in methods. Duplicate
names are rejected. Call the loader once at startup with only trusted plugins
installed; discovery imports plugin code. Since these methods are added at
runtime, static type checkers and IDEs may not discover them.
