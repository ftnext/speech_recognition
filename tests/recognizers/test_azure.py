from io import BytesIO

import pytest

import speech_recognition as sr


@pytest.mark.parametrize(
    ("key", "location", "refresh_token"),
    [
        pytest.param("key1", "westus", False, id="same-credentials"),
        pytest.param("key2", "westus", True, id="changed-key"),
        pytest.param("key1", "eastus", True, id="changed-location"),
    ],
)
def test_azure_token_cache(monkeypatch, key, location, refresh_token):
    token_requests = []
    recognition_tokens = []

    def mock_urlopen(request, timeout):
        if request.full_url.endswith("/issueToken"):
            token_requests.append(
                (request.host, request.get_header("Ocp-apim-subscription-key"))
            )
            return BytesIO(f"token{len(token_requests)}".encode())

        recognition_tokens.append(request.get_header("Authorization"))
        return BytesIO(
            b'{"RecognitionStatus":"Success","NBest":[{"Display":"hello","Confidence":1.0}]}'
        )

    monkeypatch.setattr(sr, "urlopen", mock_urlopen)
    recognizer = sr.Recognizer()
    audio_data = sr.AudioData(b"\x00\x00", 16000, 2)

    assert recognizer.recognize_azure(audio_data, "key1") == ("hello", 1.0)
    assert recognizer.recognize_azure(audio_data, key, location=location) == ("hello", 1.0)

    expected_requests = [("westus.api.cognitive.microsoft.com", "key1")]
    if refresh_token:
        expected_requests.append((f"{location}.api.cognitive.microsoft.com", key))
    assert (token_requests, recognition_tokens) == (
        expected_requests,
        ["Bearer token1", "Bearer token2" if refresh_token else "Bearer token1"],
    )
