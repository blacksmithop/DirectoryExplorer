FROM python:3.10-slim-bullseye

# work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# ignore pip as root warning
ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --user jinja2 && pip install fastapi uvicorn --no-cache-dir && apt-get autoremove -y

COPY . /code/

RUN cd auto-index && python auto-index.py /code/static/

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]