FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY wa_report.py .

CMD ["python", "wa_report.py"]
