FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src .
RUN mkdir "avatars"
CMD uvicorn main:app --host 0.0.0.0 --root-path "$ROOT_PATH"