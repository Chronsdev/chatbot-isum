FROM rasa/rasa:latest

WORKDIR /app

COPY . /app

RUN rasa train

CMD ["rasa", "run", "--enable-api", "--port", "8080", "--cors", "*"]