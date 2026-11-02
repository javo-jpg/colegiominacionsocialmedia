import sherpa_onnx, soundfile as sf, sys
d="/home/claude/asr/sherpa-onnx-whisper-small/"
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d+"small-encoder.int8.onnx",decoder=d+"small-decoder.int8.onnx",tokens=d+"small-tokens.txt",language="es",task="transcribe",num_threads=4)
x,sr=sf.read(sys.argv[1]); W=float(sys.argv[2]) if len(sys.argv)>2 else 5
t=0
while t<len(x)/sr:
    s=r.create_stream(); s.accept_waveform(sr,x[int(t*sr):int((t+W)*sr)]); r.decode_stream(s)
    print(f"{t:5.1f}-{t+W:5.1f}: {s.result.text}",flush=True); t+=W
