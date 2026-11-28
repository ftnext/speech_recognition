from speech_recognition.plugins import hookimpl


def recognize_dummy(self, audio_data):
    return f"dummy transcript ({audio_data.sample_rate} Hz)"


@hookimpl
def recognizer_methods():
    return [("recognize_dummy", recognize_dummy)]
