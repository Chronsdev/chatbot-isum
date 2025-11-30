FROM rasa/rasa:latest

# Usar un directorio diferente al de la imagen base
WORKDIR /workspace

COPY . /workspace


ENTRYPOINT []
CMD ["sh", "-c", "rasa run --enable-api --model models/20251130-182922-grim-backlist.tar.gz --port $PORT --cors '*'"]