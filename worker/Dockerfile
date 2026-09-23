FROM python:3.11-slim
WORKDIR /app
ENV PYTHONBUFFERED=1
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
CMD ["python", "worker.py"]
