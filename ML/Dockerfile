FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn joblib torch p data-science-toolkit

# CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001"]
CMD ["tail", "-f"]
