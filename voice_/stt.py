from faster_whisper import WhisperModel

print("[WHISPER] Loading model...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

print("[WHISPER] Ready")


def transcribe_file(path: str) -> str:

    segments, info = model.transcribe(
        path,
        language="ru",
        vad_filter=True
    )

    text = []

    for segment in segments:
        text.append(segment.text)

    result = " ".join(text).strip()

    print("\n[WHISPER RESULT]")
    print(result)

    return result