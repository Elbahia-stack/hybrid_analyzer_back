fROM python:3.12-slim


WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary
EXPOSE 7860


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
