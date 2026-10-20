#!/usr/bin/env python3
"""Speech to text without compiling anything (venv ~/.cache/stt, prebuilt wheels). Default engine: NVIDIA Parakeet (nemo-parakeet-tdt-0.6b-v3, via onnx-asr, ONNX Runtime);
fallback / alternative: Whisper through faster-whisper (CTranslate2, no build needed).
  ~/.cache/stt/bin/python tools/stt.py FILE.wav [--engine parakeet|whisper] [--model small]      prints the text
Audio must be a wav/flac/mp3 file (16 kHz mono is best). Models download once on first use (Hugging Face cache)."""
import sys, time
from pathlib import Path
def main():
    a = sys.argv[1:]; eng = a[a.index("--engine") + 1] if "--engine" in a else "parakeet"; mdl = a[a.index("--model") + 1] if "--model" in a else "small"
    files = [x for x in a if not x.startswith("--") and x not in (eng, mdl)]
    if not files: sys.exit(__doc__)
    t = time.time()
    if eng == "parakeet":
        try:
            import onnx_asr
            from huggingface_hub import snapshot_download
            local = snapshot_download("istupakov/parakeet-tdt-0.6b-v3-onnx", local_dir=str(Path.home() / ".cache/stt/models/parakeet-v3"))   # a real directory, not HF's symlinked cache: ONNX Runtime refuses weights outside the model folder
            m = onnx_asr.load_model("nemo-parakeet-tdt-0.6b-v3", local)
            for f in files: print(m.recognize(f))
            print(f"[parakeet {time.time() - t:.1f}s]", file=sys.stderr); return
        except Exception as e:
            print(f"[parakeet failed: {e}; falling back to whisper]", file=sys.stderr)
    from faster_whisper import WhisperModel
    w = WhisperModel(mdl, device="cpu", compute_type="int8")
    import soundfile as sf, numpy as np
    for f in files:                                                          # decode with soundfile (no PyAV needed: its newest build does not match faster-whisper)
        x, sr = sf.read(f, dtype="float32")
        if x.ndim > 1: x = x.mean(axis=1)
        if sr != 16000: x = np.interp(np.linspace(0, len(x), int(len(x) * 16000 / sr), endpoint=False), np.arange(len(x)), x).astype("float32")
        segs, _ = w.transcribe(x); print(" ".join(s.text.strip() for s in segs))
    print(f"[whisper {mdl} {time.time() - t:.1f}s]", file=sys.stderr)
main()
