FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8001","--reload"]
#CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "8", "--bind", "0.0.0.0:8000", "app.main:app"] # Scaling
#(For brevity, the other backend files like crud.py, schemas.py, etc., are as in previous messages—e.g., crud.py has all create/get functions with rating averages, wallet updates. If you need any specific one expanded, reply with the name.)
