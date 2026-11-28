OpenAI-compatible audio transcription
======================================

``recognize_openai`` works with services that accept OpenAI-compatible audio
transcription requests and return a JSON object with a ``text`` field.

Install the OpenAI integration:

.. code-block:: console

   python -m pip install "SpeechRecognition[openai]"

Set the credentials and API base URL required by your provider:

.. code-block:: console

   export OPENAI_API_KEY="your-provider-api-key"
   export OPENAI_BASE_URL="https://your-provider.example/v1"

Use a non-empty dummy key only when the endpoint does not require
authentication, such as a locally hosted service. The base URL should point
to the API root; the OpenAI SDK appends ``/audio/transcriptions``.

In both examples, set ``model`` to a transcription model ID supported by your
provider. The examples use OpenAI's ``whisper-1``. The Sakura AI Engine examples
linked below use ``whisper-large-v3-turbo``.

Stable API
----------

Use ``Recognizer.recognize_openai`` to transcribe an audio file:

.. code-block:: python

   import speech_recognition as sr

   recognizer = sr.Recognizer()
   with sr.AudioFile("audio.wav") as source:
       audio = recognizer.record(source)

   text = recognizer.recognize_openai(audio, model="whisper-1")
   print(text)

See the `complete stable API example for Sakura AI Engine
<https://gist.github.com/ftnext/84f80b060b2856d828f89a3c8b07212f>`__.

Experimental API
----------------

For lower-level access, construct ``OpenAICompatibleRecognizer`` with an
OpenAI SDK client:

.. code-block:: python

   import openai

   from speech_recognition import AudioData
   from speech_recognition.recognizers.whisper_api.openai import (
       OpenAICompatibleRecognizer,
   )

   audio = AudioData.from_file("audio.wav")
   recognizer = OpenAICompatibleRecognizer(openai.OpenAI())
   text = recognizer.recognize(audio, model="whisper-1")
   print(text)

This API is experimental and may change without notice. See the `complete
experimental API example for Sakura AI Engine
<https://gist.github.com/ftnext/bab6e5bac4500f9fb78ef6d2d0eb94b7>`__.

To use OpenAI's hosted API, set ``OPENAI_API_KEY`` and leave
``OPENAI_BASE_URL`` unset. See the `OpenAI transcription API reference
<https://developers.openai.com/api/reference/resources/audio/subresources/transcriptions/methods/create>`__.
