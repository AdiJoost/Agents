FROM python:3.13.2-slim
WORKDIR /Agents
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "run.py"]