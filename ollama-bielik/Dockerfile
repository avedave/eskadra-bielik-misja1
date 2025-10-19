FROM ollama/ollama:latest

# Listen on all interfaces, port 8080
ENV OLLAMA_HOST 0.0.0.0:8080

# Store model weight files in /models
ENV OLLAMA_MODELS /models

# Reduce logging verbosity
ENV OLLAMA_DEBUG false

# Never unload model weights from the GPU
ENV OLLAMA_KEEP_ALIVE -1

# Store the model weights in the container image
#ENV MODEL gemma3:270m
#ENV MODEL gemma3:4b
#ENV MODEL SpeakLeash/bielik-11b-v2.3-instruct:Q4_K_M
#ENV MODEL SpeakLeash/bielik-11b-v2.3-instruct:Q8_0
#ENV MODEL SpeakLeash/bielik-1.5b-v3.0-instruct:Q8_0
#ENV MODEL SpeakLeash/bielik-4.5b-v3.0-instruct:FP16
ENV MODEL SpeakLeash/bielik-4.5b-v3.0-instruct:Q8_0

RUN ollama serve & sleep 5 && ollama pull $MODEL

# Start Ollama
ENTRYPOINT ["ollama", "serve"]