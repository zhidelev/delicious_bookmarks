FROM python:3.8-alpine

COPY requirements-web.txt app/

COPY web/ app/
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements-web.txt

EXPOSE 5000:5000/tcp

RUN export FLASK_APP=app.py
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
