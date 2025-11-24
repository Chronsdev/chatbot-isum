FROM rasa/rasa:latest

# Usar un directorio diferente al de la imagen base
WORKDIR /workspace

COPY . /workspace

# Cambiar permisos en nuestro directorio (no en /app)
USER root
RUN chown -R rasa:rasa /workspace && \
    chmod -R 755 /workspace
USER rasa

ENTRYPOINT []
CMD ["sh", "-c", "rasa train && rasa run --enable-api --port $PORT --cors '*'"]