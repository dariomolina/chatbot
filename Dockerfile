FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9 AS base

WORKDIR /app

COPY ./app /app

RUN pip install -r requirements.txt

EXPOSE 80
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
