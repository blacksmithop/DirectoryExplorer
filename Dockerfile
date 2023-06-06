FROM python:3.10-slim-bullseye

# work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --user jinja2 && pip install fastapi uvicorn --no-cache-dir && apt-get autoremove -y

COPY auto-index /app/auto-index
COPY app /app/app
COPY static /app/static

RUN cd auto-index && python auto-index.py /app/static/

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]