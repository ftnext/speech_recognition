import sys
from unittest.mock import Mock

from speech_recognition import AudioData, Recognizer
from speech_recognition.recognizers.whisper_api import groq


def test_transcribe_with_groq_text_response(monkeypatch):
    client = Mock()
    create = client.audio.transcriptions.create
    create.return_value = "one two three"
    monkeypatch.setitem(sys.modules, "groq", Mock(Groq=Mock(return_value=client)))
    audio_data = AudioData(b"\x00\x00", 16000, 2)

    assert groq.recognize(Recognizer(), audio_data, response_format="text") == "one two three"
    assert create.call_args.kwargs["response_format"] == "text"
