FROM python:3.8

RUN apt-get update && apt-get install vim curl -y && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN python3 -m pip install -U pip setuptools wheel -r requirements.txt

ENV FLASK_APP=rollback
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True
EXPOSE 8080

WORKDIR /app
COPY ./ ./

CMD ["flask","run","-p","8080","-h","0.0.0.0"]