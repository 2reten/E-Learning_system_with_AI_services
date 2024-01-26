import torch
from transformers import AutoProcessor, pipeline, AutoModelForSpeechSeq2Seq

# 저장된 모델 로드
model_save_path = "whisper_model"
model = AutoModelForSpeechSeq2Seq.from_pretrained(model_save_path)

# 저장된 프로세서 로드
processor_save_path = "whisper_processor"
processor = AutoProcessor.from_pretrained(processor_save_path)

# 모델 및 파이프라인 설정
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
model.to(device)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device, )


audio_file = "C:/Users/user/desktop/trainASH00_1_006001.wav"

def convert_audio_to_text(audio_file, pipeline):
    result = pipe(audio_file)
    return result["text"]

convert_audio_to_text(audio_file, pipeline)
